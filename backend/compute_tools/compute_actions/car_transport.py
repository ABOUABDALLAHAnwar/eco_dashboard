import requests

from backend.scripts.variables import consommation, facteurs


# Distance via OSRM
def get_distance_osrm(lat1, lon1, lat2, lon2, mode="driving"):
    """
    permet de calculer les distances entre deux quartier
    Parameters
    ----------
    lat1
    lon1
    lat2
    lon2
    mode

    Returns
    -------

    """
    url = f"http://router.project-osrm.org/route/v1/{mode}/{lon1},{lat1};{lon2},{lat2}?overview=false"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        distance_m = data["routes"][0]["distance"]
        return distance_m / 1000  # km
    else:
        raise ConnectionError(f"Erreur OSRM : {response.status_code}")


def emission_voiture(distance_km: float, taille_voiture: str) -> float:
    """
    Calcule les émissions de CO₂e (en tonnes) selon la taille du véhicule et la distance parcourue.
    Facteurs d'émission issus de l'ADEME (kgCO₂e/km).
    """

    if taille_voiture not in facteurs:
        raise ValueError(
            "Taille invalide. Choisir parmi : 'petite', 'moyenne', 'grande'."
        )

    # Conversion en tonnes de CO2e
    tco2e = (distance_km * facteurs[taille_voiture]) / 1000
    return tco2e
