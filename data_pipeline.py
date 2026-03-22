from guesty_data import get_reservations, export_listings_csv, get_access_token
from unloc_data import export_locks_csv
# from unloc import unloc_headers  # Uncomment when Unloc logic is added


def get_phone_listing_dates(reservation_list):
    """Filters reservations down to phone, listingId, checkIn, and checkOut."""
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
    get_access_token()
    export_listings_csv()
    #export_locks_csv()

    #reservations = get_reservations()
    #phone_listing_data = get_phone_listing_dates(reservations)



if __name__ == "__main__":
    main()