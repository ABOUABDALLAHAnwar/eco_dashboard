import json

from fastapi import APIRouter, Depends
from backend.database import collections_handeler
from fastapi import Cookie, HTTPException

router = APIRouter(tags=["Users_dashboard"])


def get_current_user(access_token: str = Cookie(None)):
    print(access_token)

    if not access_token:
        raise HTTPException(status_code=401, detail="Token manquant")
    try:

        payload = decode_access_token(access_token)  # fonction que tu utilises pour ton JWT

        email = payload.get("sub")

        if not email:
            raise HTTPException(status_code=401, detail="Token invalide")
        return {"email": email}
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalide")

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
