import os
from pathlib import Path

from dotenv import load_dotenv

# chemin vers le .env à la racine du projet
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)


connection_uri = os.getenv("MONGO_URL", os.getenv("mongo"))
mongo = connection_uri
print(mongo)
SECRET_KEY = os.getenv("SECRET_KEY")
