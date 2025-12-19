import pytest

from backend.database import collections_handeler, handle_multiple_collections
from backend.models import users_models


def test_handle_multiple_collections(
        client_accounts_collection,
        client_actions_collection,
        user_profile_infos_collection):
    """

    Parameters
    ----------
    client_accounts_collection :
    client_actions_collection :
    user_profile_infos_collection :

    Returns
    -------

    """
    data = {
        "name": "reduce_car_use_bicycle",
        "info": {"distance": 10, "type": "moyenne"},
    }

    client_collection = collections_handeler.ClientCollection(
        client_accounts_collection
    )
    user = users_models.User(email="test@example.com", hashed_password="pass")
    client_collection.add_new_user(user)
    multiple_collections = handle_multiple_collections.MultipleCollection(
        client_accounts_collection,
        user_profile_infos_collection,
        client_actions_collection,
    )
    multiple_collections.add_user_action("test@example.com", data)
    actions = collections_handeler.ClientActions(client_actions_collection)
    act = actions.read("test@example.com")
    data2 = {
        "name": "reduce_car_use_bicycle",
        "info": {"distance": 77, "type": "moyenne"},
    }
    multiple_collections.add_user_action("test@example.com", data2)
    act2 = actions.read("test@example.com")
    print("here")

    assert act is not None
    assert act["action"][0]["tco2e_action"] == 0.0016
    assert act["tco2e_total"] == 0.0016
    assert len(act2["action"]) == 2
    assert act2["tco2e_total"] > 0.0016
