from fastapi import APIRouter, Depends

from backend.actions_templates.actions import dic_actions
from backend.compute_tools.quartier_cordonnes import get_coords
from backend.database import collections_handeler
from backend.scripts.dependencies import get_current_user

router = APIRouter(tags=["Users_dashboard"])


@router.get("/get_user_profile")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    email = current_user.get("email")
    ca = collections_handeler.UserProfileInfos()
    dte = ca.read(email)

    if dte is None:
        return {
            "name": "",
            "position": "",
            "about": "",
            "age": 0,
            "country": "",
            "address": "",
            "email": "",
            "phone": "",
            "status": "",
            "first_update_day": "",
            "first_update_hour": "",
            "last_update_day": "",
            "last_update_hour": "",
        }
    del dte["_id"]
    return dte


@router.get("/coordinates")
async def get_coordinates(current_user: dict = Depends(get_current_user)):
    email = current_user.get("email")
    ca = collections_handeler.UserProfileInfos()
    datas = ca.read(email)
    if datas is None:
        return [0, 0]
    address = datas["address"]
    print(get_coords(address))
    return get_coords(address)


@router.get("/tco2e_total")
def get_tco2e_total(current_user: dict = Depends(get_current_user)):
    """

    Parameters
    ----------
    current_user

    Returns
    -------

    """
    email = current_user.get("email")
    ca = collections_handeler.ClientActions()
    dte = ca.read(email)
    if not dte:
        return {"tco2e_total": 0, "monney": 0}

    tco2e_total = dte["tco2e_total"]
    monney = tco2e_total * 70

    return {"tco2e_total": tco2e_total, "monney": monney}


@router.get("/tco2e_evite_contributions")
def get_tco2e_contributions(current_user: dict = Depends(get_current_user)):
    """

    Parameters
    ----------
    current_user

    Returns
    -------

    """
    email = current_user.get("email")
    ca = collections_handeler.ClientActions()
    res = ca.read(email)

    total = res["tco2e_total"]
    dico = {v["name"]: 0.0 for v in dic_actions.values()}

    for item in res["action"]:
        dico[item["action"]["name"]] = (
            dico[item["action"]["name"]] + item["tco2e_action"] / total
        )

    dico = {k: float(round(v, 3)) for k, v in dico.items()}
    return dico


@router.get("/users_badges")
def get_users_badges(current_user: dict = Depends(get_current_user)):
    email = current_user.get("email")

    ca = collections_handeler.ClientActions()
    res = ca.read(email)
    total = float(res.get("tco2e_total", 0))  # tCO2e

    path = "/static/image/"
    badges = [
        {"name": "Graine d'Éveil", "threshold": 0.00001, "image": path + "00.png"},
        {"name": "Pousse Durable", "threshold": 0.25, "image": path + "10.png"},
        {"name": "Jeune Arbuste", "threshold": 1.00, "image": path + "20.png"},
        {"name": "Chêne Vigoureux", "threshold": 2.50, "image": path + "01.png"},
        {"name": "Forêt Gardienne", "threshold": 5.00, "image": path + "11.png"},
        {"name": "Légende d'Émeraude", "threshold": 10.00, "image": path + "21.png"},
    ]

    current_badge = None
    next_badge = None

    for i, badge in enumerate(badges):
        if total >= badge["threshold"]:
            current_badge = badge
            next_badge = badges[i + 1] if i + 1 < len(badges) else None
        else:
            break

    # Cas débutant (aucun badge)
    if current_badge is None:
        current_badge = {
            "name": "Aucun badge",
            "threshold": 0,
            "image": None,
        }
        next_badge = badges[0]

    # Calcul progression
    if next_badge:
        progress = (
            (total - current_badge["threshold"])
            / (next_badge["threshold"] - current_badge["threshold"])
        ) * 100
        progress = max(0, min(progress, 100))
    else:
        progress = 100  # badge max atteint

    print(current_badge)
    return {
        "tco2e_total": round(total, 3),
        "current_badge": current_badge,
        "next_badge": next_badge,
        "progress_percent": round(progress, 1),
    }
