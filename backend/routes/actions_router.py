import json

from fastapi import APIRouter, Depends

from backend.actions_templates import actions
from backend.compute_tools import quartier_cordonnes

# from backend.database import database_handeler
from backend.database import handle_multiple_collections
from backend.models.actions_models import action, action_impoved
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


@router.post("/add_actions")
def post_actions(act: action):
    """

    Parameters
    ----------
    act

    Returns
    -------

    """

    with open("data/full_actions.json") as f:
        lis = json.load(f)

    user_action = act.dict()

    quartier = user_action["quartier"]
    lat, lon = quartier_cordonnes.get_coords(quartier)
    user, name = user_action["user"], user_action["name"]
    converted_user_action = action_impoved(
        user=user,
        name=name,
        lat=lat,
        lon=lon,
        quartier=quartier,
        impact_co2_kg=0)
    lis.append(converted_user_action.dict())

    with open("data/full_actions.json", "w", encoding="utf-8") as f:
        json.dump(lis, f, ensure_ascii=False, indent=2)

    return {"message": "Action ajoutée avec succès", "total_actions": len(lis)}


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


    Parameters
    ----------
    act_info :
    current_user :

    Returns
    -------

    """

    mail = current_user.get("email")
    print(5)
    multiple_collections = handle_multiple_collections.MultipleCollection()
    print(act_info)
    user_actions = multiple_collections.add_user_action(mail, act_info)

    return {
        "message": "Action ajoutée avec succès",
        "total_actions": len(user_actions["action"]),
    }
