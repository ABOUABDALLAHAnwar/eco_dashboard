import json

from fastapi import APIRouter, Depends
from backend.database import collections_handeler
from backend.scripts.dependencies import get_current_user

router = APIRouter(tags=["Users_dashboard"])

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
        return {"tco2e_total" : 0, "monney" : 0}

    tco2e_total = dte["tco2e_total"]
    monney = tco2e_total * 70

    return {"tco2e_total" : tco2e_total, "monney" : monney}
