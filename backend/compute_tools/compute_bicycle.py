prix = 15

def emission_voiture(distance_km: float, taille_voiture: str) -> float:
    """
    Calcule les émissions de CO₂e (en tonnes) selon la taille du véhicule et la distance parcourue.
    Facteurs d'émission issus de l'ADEME (kgCO₂e/km).
    """

    # Facteurs moyens ADEME 2024
    facteurs = {
        "petite": 0.120,   # ex : citadine essence/diesel
        "moyenne": 0.160,  # ex : compacte
        "grande": 0.210    # ex : SUV
    }

    if taille_voiture not in facteurs:
        raise ValueError("Taille invalide. Choisir parmi : 'petite', 'moyenne', 'grande'.")

    # Conversion en tonnes de CO2e
    tco2e = (distance_km * facteurs[taille_voiture]) / 1000
    return tco2e

def impact_voiture(distance_km: float, taille_voiture: str, prix_essence_litre: float = 1.90) -> dict:
    """
    Calcule les émissions (tCO2e) et le coût du trajet selon la taille du véhicule.
    Données basées sur moyennes ADEME 2024 et consommation typique.
    """

    # Facteurs d'émission (kgCO2e/km)
    facteurs = {
        "petite": 0.120,
        "moyenne": 0.160,
        "grande": 0.210
    }

    # Consommation moyenne (litres / 100 km)
    consommation = {
        "petite": 5.0,
        "moyenne": 6.5,
        "grande": 8.0
    }

    if taille_voiture not in facteurs:
        raise ValueError("Taille invalide. Choisir : 'petite', 'moyenne', 'grande'.")

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
        "cout_euros": round(cout, 2)
    }


# Exemple

# Exemple d'utilisation
distance = 10  # km
taille = "moyenne"
resultat = impact_voiture(10, "moyenne")
cout = 240* resultat['cout_euros']
print(f"{240*emission_voiture(distance, taille):.4f} tCO2e, le cout evite est {cout} euros et les gains sont de "
      f"{240 * emission_voiture(distance, taille)*prix}")
