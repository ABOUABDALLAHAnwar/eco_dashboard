import pytest
from backend.database import collections_handeler
from backend.models import users_models

def test_create_user(client_accounts_collection):

    client_collection = collections_handeler.ClientCollection(client_accounts_collection)
    user = users_models.User(email="test@example.com", hashed_password="pass")
    client_collection.add_new_user(user)

    stored_user = client_accounts_collection.find_one({"email": "test@example.com"})
    assert stored_user is not None
    assert stored_user["hashed_password"] == "pass"

def test_update_user(client_accounts_collection):

    client_collection = collections_handeler.ClientCollection(client_accounts_collection)
    user = users_models.User(email="test@example.com", hashed_password="pass")
    client_collection.add_new_user(user)
    user_updated = users_models.User(email="test@example.com", hashed_password="pass")
    client_collection.update_user_connexions_info("test@example.com", user_updated)
    stored_user = client_accounts_collection.find_one({"email": "test@example.com"})
    assert stored_user is not None
    assert stored_user["hashed_password"] == "pass"



def test_add_update_user_profile_informations(user_profile_infos_collection, client_accounts_collection):
    #self, user_data
    client_collection = collections_handeler.ClientCollection(client_accounts_collection)
    user = users_models.User(email="str@gmail.com", hashed_password="pass")
    client_collection.add_new_user(user)

    client_collection = collections_handeler.UserProfileInfos(user_profile_infos_collection)
    us_model = users_models.Users_profile(name= 'str', position= 'str', about= 'str',age= 6, country= 'str',
                               address= 'str', email= 'str@gmail.com', phone= 'str', id = 'str')


    client_collection.add_update_user_informations(us_model.prof, client_accounts_collection)
    stored_user = user_profile_infos_collection.find_one({"email": "str@gmail.com"})

    assert stored_user is not None
    assert stored_user["name"] == 'str'
    #client_collection.add_update_user_informations()






