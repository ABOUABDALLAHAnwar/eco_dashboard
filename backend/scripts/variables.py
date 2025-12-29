from backend.database import database_configs

client = database_configs.client

client_accounts_collection = database_configs.client_accounts_collection
user_profile_infos_collection = database_configs.user_profile_infos_collection

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300


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
