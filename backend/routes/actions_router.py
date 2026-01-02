import json

from fastapi import APIRouter, Depends

from backend.actions_templates import actions
from backend.database import handle_multiple_collections
from backend.scripts.dependencies import get_current_user

router = APIRouter(tags=["Users_action"])


@router.get("/actions_templates")
def get_actions(act_type: str):
    """
    bicycle.json  plant_based_diet.json  public_transport.json  reduce_car_use.json  renewable_energy.json  tree_planting.json  waste_reduction.json
    Parameters
    ----------
    act_type : str

    Returns
    -------

    """

    with open(f"backend/actions_templates/{act_type}.json") as f:
        return json.load(f)


@router.get("/all_actions_templates")
def get_all_actions():
    """

    Returns
    -------

    """

    return actions.dic_actions


@router.get("/all_actions_names")
def get_all_actions():
    """

    Returns
    -------

    """

    return [act["name"] for act in actions.dic_actions.values()]


@router.get("/type_of_cars")
def get_type_of_cars():
    facteurs = ["petite", "moyenne", "grande"]
    return facteurs


@router.post("/add_user_actions")
def post_actions(
    act_info: dict, current_user: dict = Depends(get_current_user)
) -> dict:
    """{
        "name": "reduce_car_use_bicycle",
        "info": {
            "distance": 10,
            "type": "moyenne"
        }
    }
    { "name": "reduce_car_use_public_transport", "info": { "address_a": "7 rue Réné Bonnac, Cenon", "address_b" : "Aeroport Bordeaux", "type": "moyenne" } }

    { "name": "plant_based_diet", "info": { "meals_replaced": ["beef"], "meals_consumed" : ["vegan"] } }
    {
      "name": "waste_reduction",
      "info": {
        "bulk_done": true,
        "is_family": true,
        "compost_buckets": 2,
        "recycling_done": true,
        "recycling_bin_size": "large",
        "glass_trips": 1
      }
    }
    { "name": "tree_planting", "info": 1  }
    { "name": "renewable_energy", "info": "apartment"  }

    Parameters
    ----------
    act_info :
    current_user :

    Returns
    -------

    """

    mail = current_user.get("email")
    multiple_collections = handle_multiple_collections.MultipleCollection()
    user_actions = multiple_collections.add_user_action(mail, act_info)

    return {
        "message": "Action ajoutée avec succès",
        "total_actions": len(user_actions["action"]),
    }
