from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

import backend.scripts.variables as variables

# from backend.database import database_handeler
from backend.database import collections_handeler
from backend.models import users_models
from backend.scripts.dependencies import decode_access_token
from fastapi import Cookie, HTTPException


router = APIRouter(tags=["Users_profiles"])

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

@router.post("/initialise_user_profiles_old")
async def init_user_profile(
    name: str,
    position: str,
    about: str,
    age: int,
    country: str,
    address: str,
    phone: str,
    current_user: dict = Depends(get_current_user),
) -> dict:

    email = current_user.get("email")

    if variables.user_profile_infos_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already exists.")

    _id = str(variables.client_accounts_collection.find_one(
        {"email": email})["_id"])
    us_model = users_models.Users_profile(
        name, position, about, age, country, address, phone, email, _id
    )

    userprofiles = collections_handeler.UserProfileInfos()
    userprofiles.add_update_user_informations(us_model.prof)

    return us_model.prof_dict

@router.post("/initialise_user_profiles")
async def init_user_profile(
    profile: users_models.UserProfileIn,  # ← FastAPI attend du JSON automatiquement
    current_user: dict = Depends(get_current_user),
) -> dict:

    email = current_user.get("email")
    if variables.user_profile_infos_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Profil déjà initialisé pour cet email.")

    _id = str(variables.client_accounts_collection.find_one({"email": email})["_id"])
    us_model = users_models.Users_profile(
        profile.name, profile.position, profile.about, profile.age,
        profile.country, profile.address, profile.phone, email, _id
    )
    userprofiles = collections_handeler.UserProfileInfos()
    userprofiles.add_update_user_informations(us_model.prof)
    return us_model.prof_dict

@router.post("/update_user_profiles")
async def update_user_profile(
    dict_update: dict, current_user: dict = Depends(get_current_user)
) -> dict:

    email = current_user.get("email")

    return dict_update
