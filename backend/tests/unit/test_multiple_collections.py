import pytest

from backend.database import collections_handeler, handle_multiple_collections
from backend.models import users_models


def test_handle_multiple_collections(
    client_accounts_collection, client_actions_collection, user_profile_infos_collection
):
    """

    Parameters
    ----------
    client_accounts_collection :
    client_actions_collection :
    user_profile_infos_collection :

    Returns
    -------

    """
    profile = {
        "name": "Dr. Mohamed Anwar ABOUABDALLAH",
        "position": "Data scientist",
        "about": "Mathématicien/informaticien passionné, doté d’un raisonnement analytique affûté et d’excellentes compétences relationnelles. Fortement intéressé par l’IA (NLP/LLM), le cloud et le déploiement de solutions ML industrielles. Diplômé ingénieur en 2019 et docteur en 2022, j’ai développé des projets variés allant de la data engineering à la data science appliquée, en concevant, entraînant et déployant des modèles ML en production pour optimiser des processus métier et générer de la valeur opérationnelle.",
        "age": 29,
        "country": "France",
        "address": "7 Rue René Bonnac, Cenon",
        "email": "test@example.com",
        "phone": "0758808906",
    }

    data = {
        "name": "reduce_car_use_public_transport",
        "info": {
            "address_a": "7 rue Réné Bonnac, Cenon",
            "address_b": "Aeroport Bordeaux",
            "type": "moyenne",
        },
    }

    client_collection = collections_handeler.ClientCollection(
        client_accounts_collection
    )
    user = users_models.User(email="test@example.com", hashed_password="pass")
    client_collection.add_new_user(user)

    upc = collections_handeler.UserProfileInfos(user_profile_infos_collection)
    upc.create(profile)
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
        "info": {
            "address_a": "7 rue Réné Bonnac, Cenon",
            "address_b": "Aeroport Bordeaux",
            "type": "moyenne",
        },
    }

    multiple_collections.add_user_action("test@example.com", data2)
    act2 = actions.read("test@example.com")

    assert act is not None
    assert act["action"][0]["tco2e_action"] == 0.0029873579999999994
    assert act["tco2e_total"] == 0.0029873579999999994
    assert len(act2["action"]) == 2
    assert act2["tco2e_total"] > 0.0029873579999999994
