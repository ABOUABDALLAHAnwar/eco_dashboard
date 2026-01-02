import json

from fastapi import APIRouter, Depends

from backend.routes.full_data_router import (
    get_coordinate_city,
    get_dashboard_full_data,
)
from backend.routes.users_dashboard_router import (
    get_coordinates,
    get_tco2e_contributions,
    get_tco2e_total,
    get_user_profile,
    get_users_badges,
)
from backend.scripts.dependencies import get_current_user
from backend.services.cache_service import (
    r,  # On importe ton client Redis config
)

router = APIRouter(tags=["Cached_Dashboard"])


@router.get("/get_dashboard_snapshot")
async def get_dashboard_snapshot(current_user: dict = Depends(get_current_user)):
    email = current_user.get("email")
    cache_key = f"user_snapshot:{email}"

    # 1. Tenter de récupérer depuis Redis
    cached_data = r.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    # 2. Si rien en cache, on appelle tes fonctions une par une
    # On utilise "await" car certaines de tes fonctions sont async

    profile = await get_user_profile(current_user)
    coords = await get_coordinates(current_user)
    impact = get_tco2e_total(current_user)  # Ta fonction n'est pas async
    contributions = get_tco2e_contributions(current_user)  # Ta fonction n'est pas async
    badges = get_users_badges(current_user)  # Ta fonction n'est pas async

    # On prépare le gros dictionnaire
    snapshot = {
        "profile": profile,
        "coordinates": coords,
        "tco2e": impact,
        "contributions": contributions,
        "badges": badges,
    }

    # 3. On enregistre dans Redis pour 5 minutes
    r.setex(cache_key, 300, json.dumps(snapshot))

    return snapshot


@router.get("/get_cached_city_markers")
async def get_cached_city_markers():
    cache_key = "global_city_markers"

    # 1. Vérifier si Redis a les marqueurs
    cached = r.get(cache_key)
    if cached:
        print("🚀 CITY CACHE HIT")
        return json.loads(cached)

    # 2. Si non, on récupère les données de base (Ville, Count, CO2)

    raw_cities = await get_dashboard_full_data()

    # 3. On enrichit avec les coordonnées GPS
    enriched_markers = []
    for city_name, count, co2 in raw_cities:
        coords = await get_coordinate_city(city_name)
        enriched_markers.append(
            {"name": city_name, "count": count, "co2": co2, "coords": coords}
        )

    # 4. On stocke dans Redis pour 1 heure (les villes ne bougent pas souvent !)
    r.setex(cache_key, 3600, json.dumps(enriched_markers))

    return enriched_markers
