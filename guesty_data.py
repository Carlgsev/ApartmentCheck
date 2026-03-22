from dotenv import load_dotenv
import requests
import os
import pandas as pd

load_dotenv("guesty.env")

guesty_client_ID = os.getenv("CLIENT_ID")
guesty_client_secret = os.getenv("CLIENT_SECRET")


def get_access_token():
    env_path = "guesty.env"
    
    token_response = requests.post(
        "https://open-api.guesty.com/oauth2/token",
        data={
            "grant_type": "client_credentials",
            "client_id": guesty_client_ID,
            "client_secret": guesty_client_secret,
        }
    )
    token_data = token_response.json()
    token = token_data.get("access_token")
    if not token:
        raise ValueError(f"Failed to get access token: {token_data}")

    
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(f"CLIENT_ID={guesty_client_ID}\n")
        f.write(f"CLIENT_SECRET={guesty_client_secret}\n")
        f.write(f"GUESTY_TOKEN={token}\n")

    


import json
import os

def export_listings_csv():
    token = os.getenv("GUESTY_TOKEN")
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    response = requests.get(
        "https://open-api.guesty.com/v1/listings",
        headers=headers
    )
    if response.status_code != 200:
        print(f"Failed to fetch listings: {response.status_code} - {response.text}")
        return

    data = response.json()
    listings = data.get("results", [])

    if not listings:
        print("No listings found.")
        return

    # Save the raw JSON to a file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "listings_raw.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(listings, f, indent=4)

    print(f"✅ Raw listings exported to: {output_path}")

def get_reservations():
    """Fetches all reservations from Guesty and returns them as a list."""
    token = get_access_token()
    listing_id = "69a3602adb141046778e0aee"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    all_reservations = []
    limit = 100
    response = requests.get(
        "https://open-api.guesty.com/v1/listings/{listing_id}",
        headers=headers,
        params={"limit": limit},
    )
    if response.status_code == 200:
        data = response.json()
        reservations = data.get("results", [])
        all_reservations.extend(reservations)
    else:
        print(f"Failed to fetch reservations: {response.status_code} - {response.text}")
    return all_reservations

#Test