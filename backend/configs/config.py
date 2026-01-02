import os
from pathlib import Path

from dotenv import load_dotenv

# chemin vers le .env à la racine du projet
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)


connection_uri = os.getenv("MONGO_URL", os.getenv("mongo"))
mongo = connection_uri
SECRET_KEY = os.getenv("SECRET_KEY")


# Récupérer les variables
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
