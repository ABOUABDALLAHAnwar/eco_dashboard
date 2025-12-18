from datetime import datetime, timedelta
from typing import Optional

import jwt
import requests
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

import backend.variables as variables
from backend.configs import config
from backend.database import database_handeler
from backend.models import users_models
from backend.users_handler import handle_users


def time_creation():

    update_time = datetime.utcnow()
    formatted_time = update_time.strftime("%m/%d/%Y/%H/%M/%S")
    return formatted_time


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=variables.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, config.SECRET_KEY, algorithm=variables.ALGORITHM
    )
    return encoded_jwt


router = APIRouter()


@router.post("/signup")  # , response_class=HTMLResponse
async def signup(
    request: Request, email: str, password: str
):  # = Form(...) dans email et passeword

    if variables.client_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already exists.")

    usersign = handle_users.UserSignin(password)
    hashed_password = usersign.hashed
    user = users_models.User(
        email=email, hashed_password=hashed_password
    )  # {"email": email, "hashed_password": hashed_password}

    database_handeler.add_new_user(user)

    return user.email


@router.post("/password")  # , response_class=HTMLResponse  /login
async def signin(
    request: Request,
    # response: Response,
    email: str,  # = Form(...),
    password: str,  # = Form(...),
):
    user = variables.client_collection.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if not handle_users.verify_password(password, user["hashed_password"]):
        # raise HTTPException(status_code=401, detail="Invalid credentials.")
        return "faux mdp"

    access_token = create_access_token(data={"sub": email})

    # Redirect to dashboard

    # Add the cookie to the redirect response

    return email
