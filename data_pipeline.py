from dotenv import load_dotenv
import requests
import os


load_dotenv("guesty.env")
load_dotenv("unloc.env")

#Code block for client secret verification and token retrieval
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
token_data = token_response.json()
print(token_data)
token = token_response.json()["access_token"]
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

# Code block for Unloc client credential authentication
unloc_client_ID = os.getenv("UNLOC_CLIENT_ID")
unloc_client_secret = os.getenv("UNLOC_CLIENT_SECRET")

unloc_token_response = requests.post(
    "https://api.unloc.app/oauth/token",
    data={
        "grant_type": "client_credentials",
        "client_id": unloc_client_ID,
        "client_secret": unloc_client_secret,
    }
)

unloc_token_data = unloc_token_response.json()
print(unloc_token_data)

unloc_token = unloc_token_data.get("access_token")

unloc_headers = {
    "Authorization": f"Bearer {unloc_token}",
    "Accept": "application/json"
}

#Appends all data for all reservations onto a list which is then later filtered into the result list
#Which only contains the desired data
#limit is upper threshold of how many reservations can be retrieved
#
def get_reservations():
    all_reservations = []

    limit = 100 

    response = requests.get(
        "https://open-api.guesty.com/v1/reservations",
        headers=headers,
        params={
            "limit": limit,
            
        }
    )
    data = response.json()
    
    reservations = data.get("results", [])    
    all_reservations.extend(reservations)

    for reservation in all_reservations:
        print(reservation)
    
    return all_reservations


def get_phone_listing_dates(reservation_list):
    result = []

    for reservation in reservation_list:
        listing_id = reservation.get("listingId")
        check_in = reservation.get("checkIn")
        check_out = reservation.get("checkOut")

        guest = reservation.get("guest", {})
        phone = guest.get("phone")

        if phone and listing_id:
            result.append({
                "phone": phone,
                "listingId": listing_id,
                "checkIn": check_in,
                "checkOut": check_out
            })

    return result

def main():
    reservations = get_reservations()
    phone_listing_data = get_phone_listing_dates(reservations)
    for entry in phone_listing_data:
        print(entry)
  
if __name__ == "__main__":
    main()

#Issues:
#Unloc requires a lock id when creating keys. 
#If it's 1 lock per apartment, fix this by doing a dictionary with apartmentID : Lock ID(s)
