from collections import defaultdict

from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim

from backend.compute_tools.quartier_cordonnes import get_coords
from backend.database import collections_handeler, database_configs

# ----------------------------
# Setup
# ----------------------------

client_actions_collection = database_configs.client_actions_collection
userProfileInfos = collections_handeler.UserProfileInfos()

geolocator = Nominatim(user_agent="eco-dashboard-test")


# ----------------------------
# Utils
# ----------------------------


def coords_to_city(lat: float, lon: float) -> str | None:
    try:
        location = geolocator.reverse((lat, lon), zoom=10, language="fr")
        if not location:
            return None

        address = location.raw.get("address", {})
        return (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("municipality")
        )

    except GeocoderTimedOut:
        return None


# ----------------------------
# Extraction brute
# ----------------------------
def extract_datas():
    raw_data = [
        [
            doc["email"],
            doc["tco2e_total"],
            get_coords(userProfileInfos.read(doc["email"])["address"]),
        ]
        for doc in client_actions_collection.find(
            {}, {"email": 1, "tco2e_total": 1, "_id": 0}
        )
    ]
    return raw_data


# ----------------------------
# Agrégations demandées
# ----------------------------
def aggregate_datas():
    users_per_city = defaultdict(set)
    tco2e_per_city = defaultdict(float)
    coords_cache = {}
    raw_data = extract_datas()

    for email, tco2e, (lat, lon) in raw_data:

        if (lat, lon) not in coords_cache:
            coords_cache[(lat, lon)] = coords_to_city(lat, lon)

        city = coords_cache[(lat, lon)]

        users_per_city[city].add(email)
        tco2e_per_city[city] += tco2e

    return users_per_city, tco2e_per_city


def coords_to_neighbourhood(lat: float, lon: float) -> str | None:
    try:
        location = geolocator.reverse((lat, lon), zoom=18, language="fr")
        if not location:
            return None

        address = location.raw.get("address", {})

        neighbourhood = (
            address.get("neighbourhood")
            or address.get("suburb")
            or address.get("quarter")
            or address.get("borough")
            or address.get("district")
        )

        # 🔴 RÈGLE MÉTIER MANQUANTE
        if not neighbourhood:
            city = (
                address.get("city")
                or address.get("town")
                or address.get("village")
                or address.get("municipality")
            )
            if city:
                return f"{city} Centre"

        return neighbourhood

    except GeocoderTimedOut:
        return None


def aggregate_by_neighbourhood():
    users_per_neighbourhood = defaultdict(set)
    tco2e_per_neighbourhood = defaultdict(float)
    coords_cache = {}

    raw_data = extract_datas()

    for email, tco2e, (lat, lon) in raw_data:

        if (lat, lon) not in coords_cache:
            coords_cache[(lat, lon)] = coords_to_neighbourhood(lat, lon)

        neighbourhood = coords_cache[(lat, lon)]
        if not neighbourhood:
            continue

        users_per_neighbourhood[neighbourhood].add(email)
        tco2e_per_neighbourhood[neighbourhood] += tco2e

    return [
        [
            neighbourhood,
            len(users_per_neighbourhood[neighbourhood]),
            tco2e_per_neighbourhood[neighbourhood],
        ]
        for neighbourhood in users_per_neighbourhood
    ]
