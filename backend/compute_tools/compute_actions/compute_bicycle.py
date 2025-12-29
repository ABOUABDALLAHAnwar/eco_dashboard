from backend.compute_tools import quartier_cordonnes
from backend.compute_tools.compute_actions import car_transport
from backend.scripts.variables import consommation, facteurs

prix = 15


def impact_voiture(
    address_a: str,
    address_b: str,
    taille_voiture: str,
    prix_essence_litre: float = 1.90,
) -> dict:
    """
    Calcule les émissions (tCO2e) et le coût du trajet selon la taille du véhicule.
    Données basées sur moyennes ADEME 2024 et consommation typique.
    """

    if taille_voiture not in facteurs:
        raise ValueError("Taille invalide. Choisir : 'petite', 'moyenne', 'grande'.")

    lat1, lon1 = quartier_cordonnes.get_coords(address_a)
    lat2, lon2 = quartier_cordonnes.get_coords(address_b)

    # Distance sur route
    distance_km = car_transport.get_distance_osrm(
        lat1, lon1, lat2, lon2, mode="driving"
    )
    # Émissions en tonnes de CO2e
    tco2e = (distance_km * facteurs[taille_voiture]) / 1000

    # Consommation et coût
    litres = distance_km * consommation[taille_voiture] / 100
    cout = litres * prix_essence_litre

    return {
        "distance_km": distance_km,
        "taille_voiture": taille_voiture,
        "emissions_tCO2e": round(tco2e, 4),
        "carburant_litres": round(litres, 2),
        "cout_euros": round(cout, 2),
    }


# Exemple

"""# Exemple d'utilisation
distance = 10  # km
taille = "moyenne"
resultat = impact_voiture(10, "moyenne")
cout = 240* resultat['cout_euros']
print(f"{240*emission_voiture(distance, taille):.4f} tCO2e, le cout evite est {cout} euros et les gains sont de "
      f"{240 * emission_voiture(distance, taille)*prix}")
"""
