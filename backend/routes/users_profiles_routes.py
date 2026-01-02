from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)

import backend.scripts.variables as variables
from backend.database import collections_handeler
from backend.models import users_models
from backend.scripts.dependencies import get_current_user

router = APIRouter(tags=["Users_profiles"])


@router.post("/initialise_user_profiles")
async def init_user_profile(
    profile: users_models.UserProfileIn,  # ← FastAPI attend du JSON automatiquement
    current_user: dict = Depends(get_current_user),
) -> dict:

    email = current_user.get("email")

    _id = str(variables.client_accounts_collection.find_one({"email": email})["_id"])
    us_model = users_models.UsersProfile(
        profile.name,
        profile.position,
        profile.about,
        profile.age,
        profile.country,
        profile.address,
        profile.phone,
        email,
        _id,
    )
    """if variables.user_profile_infos_collection.find_one({"email": email}):
        print("exist")
        raise HTTPException(
            status_code=400, detail="Profil déjà initialisé pour cet email."
        )"""

    userprofiles = collections_handeler.UserProfileInfos()

    userprofiles.add_update_user_informations(us_model.prof)

    return us_model.prof_dict
