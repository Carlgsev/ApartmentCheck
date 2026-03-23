from dotenv import load_dotenv
import requests
import os
import csv

load_dotenv("unloc.env")

unloc_client_ID = os.getenv("UNLOC_CLIENT_ID")
unloc_client_secret = os.getenv("UNLOC_CLIENT_SECRET")
unloc_token = os.getenv("UNLOC_TOKEN")

PROJECT_ID = "555f5120-1427-43c0-87fd-d23b2cc986a3"

def get_unloc_token():
    response = requests.post(
        "https://api.unloc.app/v2/auth/token/",
        data={
            "grant_type": "client_credentials",
            "client_id": unloc_client_ID,
            "client_secret": unloc_client_secret,
            "project_id": PROJECT_ID,
            "scope": "project.admin",
        }
    )
    token_data = response.json()
    token = token_data.get("access_token")
    if token:
        with open("unloc.env", "w") as f:
            f.write(f"UNLOC_CLIENT_ID={unloc_client_ID}\n")
            f.write(f"UNLOC_CLIENT_SECRET={unloc_client_secret}\n")
            f.write(f"UNLOC_TOKEN={token}\n")
    return token

if not unloc_token:
    unloc_token = get_unloc_token()

unloc_headers = {
    "Authorization": f"Bearer {unloc_token}",
    "Accept": "application/json"
}


def get_locks():
    """Fetches all locks for project V51 from Unloc."""
    global unloc_token, unloc_headers
    response = requests.get(
        f"https://api.unloc.app/v2/projects/{PROJECT_ID}/locks",
        headers=unloc_headers
    )
    if response.status_code == 401:
        # Token invalid or expired, get a new one and retry once
        unloc_token = get_unloc_token()
        unloc_headers = {
            "Authorization": f"Bearer {unloc_token}",
            "Accept": "application/json"
        }
        response = requests.get(
            f"https://api.unloc.app/v2/projects/{PROJECT_ID}/locks",
            headers=unloc_headers
        )
    if response.status_code == 200:
        data = response.json()
        locks = data if isinstance(data, list) else data.get("results", data.get("locks", []))
        return locks
    else:
        print(f"Failed to fetch locks: {response.status_code} - {response.text}")
        return []


def export_locks_csv():
    """Fetches locks for project and exports all info to locks.csv"""
    locks = get_locks()
    if not locks:
        print("No locks found to export.")
        return

    # Get all unique keys across all locks
    all_keys = set()
    for lock in locks:
        all_keys.update(lock.keys())
    all_keys = list(all_keys)  # convert to list for CSV

    # Prepare CSV file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "locks.csv")

    with open(output_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=all_keys)
        writer.writeheader()
        for lock in locks:
            writer.writerow(lock)

    print(f"Locks exported to: {output_path}")


# Issues:
# Unloc requires a lock id when creating keys.
# If it's 1 lock per apartment, fix this by doing a dictionary with apartmentID : Lock ID(s)