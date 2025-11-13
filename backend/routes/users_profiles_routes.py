from fastapi import APIRouter
from backend.models import users_models
from fastapi import APIRouter, HTTPException, Request, Depends, Response, status
from backend.dependencies import get_current_user
import backend.variables as variables
from backend.database import database_handeler
router = APIRouter(tags=["Users_profiles"])

@router.post("/initialise_user_profiles")
async def init_user_profile(name: str,
                            position: str,
                            about: str,
                            age: int,
                            country: str,
                            address: str,
                            phone: str,
                            current_user: dict = Depends(get_current_user)
                            ) -> dict:

    email = current_user.get("email")
    if variables.user_profile_infos_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already exists.")


    print(variables.client_collection.find_one({"email": email}))
    _id = str(variables.client_collection.find_one({"email": email})['_id'])
    us_model = users_models.Users_profile(
        name, position, about, age,
        country, address, phone, email, _id)
    print(us_model.prof_dict)
    database_handeler.add_update_user_informations(us_model.prof)



    return us_model.prof_dict
