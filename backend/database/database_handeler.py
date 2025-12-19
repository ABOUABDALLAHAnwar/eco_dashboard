from bson import ObjectId
from fastapi import HTTPException
from pymongo import MongoClient

from backend.configs import config
from backend.database import database

"""#from handle_users import users_storage as storages"""

client_collection = database.client_collection
client_infos_collection = database.client_infos_collection
user_profile_infos_collection = database.user_profile_infos_collection


def find_users_datas(email, collection):
    """

    Parameters
    ----------
    email :
    collection :

    Returns
    -------

    """

    document = collection.find_one({"email": email})

    return document


def add_new_user(user):
    """

    Parameters
    ----------
    user :

    Returns
    -------

    """

    email = user.model_dump()["email"]
    document = find_users_datas(email, client_collection)

    if document is not None:
        raise HTTPException(status_code=400, detail="Email already exists.")

    else:
        client_collection.insert_one(user.model_dump())


def add_update_user_informations(user_data):
    """

    Parameters
    ----------
    user_data :

    Returns
    -------

    """

    email = user_data.model_dump()["email"]
    id = database.client_collection.find_one({"email": email})["_id"]

    document = find_users_datas(email, database.user_profile_infos_collection)

    if document is not None:
        user_data_dict = user_data.model_dump()
        user_data_dict["_id"] = document["_id"]
        client_infos_collection.replace_one(
            {"_id": ObjectId(document["_id"])}, user_data_dict
        )
    else:
        user_data_dict = user_data.model_dump()
        user_data_dict["_id"] = id
        client_infos_collection.insert_one(user_data_dict)


def add_update_user_profile_informations(user_data):
    """

    Parameters
    ----------
    user_data :

    Returns
    -------

    """

    email = user_data["email"]  # .model_dump()
    document = find_users_datas(email, user_profile_infos_collection)

    if document is not None:
        user_profile_infos_collection.delete_one({"email": email})

    user_profile_infos_collection.insert_one(user_data)  # .model_dump()


def get_update_user_profile_informations(email):
    """

    Parameters
    ----------
    email :

    Returns
    -------

    """
    document = find_users_datas(email, user_profile_infos_collection)
    return document


def get_all_datas(email):
    """

    Parameters
    ----------
    email :

    Returns
    -------

    """

    client_information = find_users_datas(email, client_infos_collection)

    user_profile = find_users_datas(email, user_profile_infos_collection)

    result = {
        "client_information": client_information,
        "user_profile": user_profile,
    }

    return result
