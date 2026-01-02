# Facteurs moyens ADEME 2024
facteurs = {
    "petite": 0.120,  # ex : citadine essence/diesel
    "moyenne": 0.160,  # ex : compacte
    "grande": 0.210,  # ex : SUV
}

# Consommation moyenne (litres / 100 km)
consommation = {"petite": 5.0, "moyenne": 6.5, "grande": 8.0}

factors = {
    "petite": 0.120,  # citadine
    "moyenne": 0.160,  # compacte
    "grande": 0.210,  # SUV
    "bus": 0.05,
    "tram": 0.03,
    "train": 0.04,
    "cycling": 0.0,
    "walking": 0.0,
    "public": 0.05,
}

FOOD_COEFFICIENTS = {
    "beef": 6.50,
    "lamb": 6.40,
    "pork": 1.10,
    "veal": 1.15,
    "chicken": 0.80,
    "fish": 1.20,
    "cheese": 0.35,  # Pour une portion
    "vegetarian": 0.55,  # Avec oeufs/laitage
    "vegan": 0.40,
}

# Gain de CO2e par geste (en kg)
# Ces valeurs sont des moyennes par "acte" de tri ou de réduction
WASTE_FACTORS = {"compost": 1.5, "recycling": 2.0, "glass": 0.8, "bulk_shopping": 1.2}
