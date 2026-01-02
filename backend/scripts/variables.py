from backend.database import database_configs

client = database_configs.client

client_accounts_collection = database_configs.client_accounts_collection
user_profile_infos_collection = database_configs.user_profile_infos_collection

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300
