
print("s")
from dotenv import load_dotenv
import requests
import os

load_dotenv("guesty.env")

guesty_client_ID = os.getenv("CLIENT_ID")
guesty_client_secret = os.getenv("CLIENT_SECRET")

token_response = requests.post(
    "https://open-api.guesty.com/oauth2/token",
    data={
        "grant_type": "client_credentials",
        "client_id": guesty_client_ID,
        "client_secret": guesty_client_secret,
    }
)

token = token_response.json()["access_token"]


headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

def get_reservations():
    all_reservations = []
    skip = 0
    limit = 100 

    response = requests.get(
        "https://open-api.guesty.com/v1/reservations",
        headers=headers,
        params={
            "limit": limit,
            "skip": skip
        }
    )
    data = response.json()
    
    reservations = data.get("results", [])    
    all_reservations.extend(reservations)

    result = []
    for reservation in all_reservations:
        guest_id = reservation.get("guestId")
        check_in = reservation.get("checkIn")
        check_out = reservation.get("checkOut")
        result.append({
            "guestId": guest_id,
            "checkInDate": check_in,
            "checkOutDate": check_out
        })
    return result

def main():
    reservations = get_reservations()
  
if __name__ == "__main__":
    main()
