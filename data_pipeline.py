from guesty_data import get_reservations, export_listings_csv, get_access_token, extract_apartment_number
from unloc_data import export_locks_csv
import json
import os
import requests


PROJECT_ID = "555f5120-1427-43c0-87fd-d23b2cc986a3"

def give_access(lock_id, app_user_id, checkin, checkout):
    unloc_token = os.getenv("UNLOC_TOKEN")

    headers = {
        "Authorization": f"Bearer {unloc_token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # app_user_id must be a valid Unloc app user ID
    payload = {
        "keys": [
            {
                "lockId": lock_id,
                "appUserId": app_user_id, 
                "startTime": checkin,
                "endTime": checkout
            }
        ]
    }

    url = f"https://api.unloc.app/v2/projects/{PROJECT_ID}/keys"
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("Access granted:", response.json())
        return response.json()
    return response.json()

def main():
    with open("dictionary.json", "r", encoding="utf-8") as f:
        apartment_dict = json.load(f)
    
    temp_phone = "+46708675462"
    temp_checkin = "2026-03-22T14:00:00.000Z"
    temp_checkout= "2026-03-23T14:00:00.000Z"
    temp_id = "696f67d25663fb004346879f"
    temp_lock_id = apartment_dict.get(temp_id)

    if temp_lock_id:
        give_access(temp_lock_id, temp_phone, temp_checkin, temp_checkout)
    else:
        print(f"No lock ID found for reservation ID {temp_id}")

if __name__ == "__main__":
    main()