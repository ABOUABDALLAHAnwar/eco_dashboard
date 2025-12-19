import os
from dotenv import load_dotenv
from pathlib import Path


# chemin vers le .env à la racine du projet
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

mongo = os.getenv("mongo")

SECRET_KEY = os.getenv("SECRET_KEY")
