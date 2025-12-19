import datetime

from bson import ObjectId
from fastapi import HTTPException

from backend.compute_tools import compute_bicycle
from backend.database import database_configs

client_accounts_collection = database_configs.client_accounts_collection
client_infos_collection = database_configs.client_actions_collection
user_profile_infos_collection = database_configs.user_profile_infos_collection


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
    document = find_users_datas(email, client_accounts_collection)

    if document is not None:
        raise HTTPException(status_code=400, detail="Email already exists.")

    else:
        client_accounts_collection.insert_one(user.model_dump())


def add_update_user_informations(user_data):
    """

    Parameters
    ----------
    user_data :

    Returns
    -------

    """

    email = user_data.model_dump()["email"]
    id = database_configs.client_accounts_collection.find_one({"email": email})[
        "_id"]

    document = find_users_datas(
        email, database_configs.user_profile_infos_collection)

    if document is not None:
        user_data_dict = user_data.model_dump()
        user_data_dict["_id"] = document["_id"]
        user_profile_infos_collection.replace_one(
            {"_id": ObjectId(document["_id"])}, user_data_dict
        )
    else:
        user_data_dict = user_data.model_dump()
        user_data_dict["_id"] = id
        user_profile_infos_collection.insert_one(user_data_dict)


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


def add_user_action(mail, act_info):
    """

    Parameters
    ----------
    mail :
    act_info :

    Returns
    -------

    """
    user_profile = find_users_datas(mail, user_profile_infos_collection)
    user_actions = find_users_datas(mail, client_infos_collection)

    tco2e_action_per_action = 0
    if "name" in act_info.keys(
    ) and act_info["name"] == "reduce_car_use_bicycle":
        tco2e_action_per_action = compute_bicycle.impact_voiture(
            act_info["info"]["distance"], act_info["info"]["type"]
        )["emissions_tCO2e"]

    if user_actions is None:
        user_actions = {
            "_id": user_profile["_id"],
            "first_update_hour": [
                datetime.datetime.now().time().hour,
                datetime.datetime.now().time().minute,
                datetime.datetime.now().time().second,
            ],
            "action": [
                dict(
                    action_date=[
                        datetime.datetime.now().time().hour,
                        datetime.datetime.now().time().minute,
                        datetime.datetime.now().time().second,
                    ],
                    action=act_info,
                    tco2e_action=tco2e_action_per_action,
                )
            ],
            "tco2e_total": tco2e_action_per_action,
            "email": mail,
        }
        client_infos_collection.insert_one(user_actions)

    else:
        user_actions["action"].append(
            dict(
                action_date=[
                    datetime.datetime.now().time().hour,
                    datetime.datetime.now().time().minute,
                    datetime.datetime.now().time().second,
                ],
                action=act_info,
                tco2e_action=tco2e_action_per_action,
            )
        )

        user_actions["tco2e_total"] = (
            user_actions["tco2e_total"] + user_actions["action"][-1]["tco2e_action"]
        )
        client_infos_collection.update_one(
            {"_id": user_profile["_id"]},  # filtre pour le document
            {"$set": user_actions},  # mise à jour complète du document
        )
        # client_infos_collection.update_one(user_actions)

    return user_actions
