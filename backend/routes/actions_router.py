from fastapi import APIRouter
import json
from backend.models.actions_models import action, action_impoved
from backend.compute_tools import quartier_cordonnes
router = APIRouter()


@router.get("/actions")
def get_actions():
    with open("data/mock_actions.json") as f:
        return json.load(f)

"""@router.get("/user_action/{username}")
def get_my_actions(username:str):
    with open("data/full_actions.json") as f:
        list = json.load(f)
    
    resulting_list = [[my_action["name"], my_action["impact_co2_kg"]] ]"""

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
        list = json.load(f)

    user_action = act.dict()

    quartier = user_action['quartier']
    lat, lon = quartier_cordonnes.get_coords(quartier)
    user, name = user_action['user'], user_action['name']
    converted_user_action = action_impoved(
        user=user,
        name=name,
        lat=lat,
        lon=lon,
        quartier=quartier,
        impact_co2_kg=0)
    list.append(converted_user_action.dict())

    with open("data/full_actions.json", "w", encoding="utf-8") as f:
        json.dump(list, f, ensure_ascii=False, indent=2)

    return {"message": "Action ajoutée avec succès", "total_actions": len(list)}
