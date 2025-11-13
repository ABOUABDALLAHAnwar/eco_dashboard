import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

mongo = os.getenv("mongo")
SECRET_KEY = os.getenv("SECRET_KEY")
