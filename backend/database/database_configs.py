from pymongo import MongoClient

from backend.configs import config

uri = config.mongo

client = MongoClient(uri)

db = client["app_eco_part"]
client_accounts_collection = db["client_accounts"]
client_actions_collection = db["client_actions"]
user_profile_infos_collection = db["user_profile"]
