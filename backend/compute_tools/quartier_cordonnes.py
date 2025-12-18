from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim


def get_coords(address):
    geolocator = Nominatim(user_agent="eco_dashboard")
    try:
        location = geolocator.geocode(address, timeout=10)  # délai augmenté
        if location:
            return location.latitude, location.longitude

        else:
            print("Adresse introuvable.")
    except GeocoderTimedOut:
        print("⚠️ Timeout — le service a mis trop de temps à répondre.")
