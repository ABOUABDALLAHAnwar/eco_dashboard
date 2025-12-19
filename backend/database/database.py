from fastapi import HTTPException
from pymongo import MongoClient

from backend.configs import config

"""#from handle_users import users_storage as storages"""

uri = config.mongo

client = MongoClient(uri)
db = client["app_eco_part"]
client_collection = db["client"]
client_infos_collection = db["client_information"]
user_profile_infos_collection = db["user_profile"]
