from pymongo import MongoClient

from backend.database import database

client = database.client

client_collection = database.client_collection
user_profile_infos_collection = database.user_profile_infos_collection

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300
