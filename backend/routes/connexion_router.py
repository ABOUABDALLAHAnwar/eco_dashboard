from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

import backend.scripts.variables as variables
from backend.configs import config
from backend.database import collections_handeler
from backend.scripts.dependencies import get_current_user
from backend.models import users_models
from backend.users_handler import handle_users

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------

router = APIRouter(tags=["Authentication"])


SECRET_KEY = config.SECRET_KEY
ALGORITHM = variables.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = variables.ACCESS_TOKEN_EXPIRE_MINUTES


# ---------------------------------------------------------------------
# UTILS
# ---------------------------------------------------------------------


def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None) -> str:
    """
    function to create access tokens,
    Parameters
    ----------
    data : dict
    expires_delta :

    Returns
    -------
    access tohen in str format

    """

    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ---------------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------------
@router.post("/signup", status_code=201)
async def signup(email: str, password: str) -> dict:
    """
    sign up function
    Parameters
    ----------
    email : string
    password : string

    Returns
    -------

    """
    if variables.client_accounts_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already exists.")

    hashed_password = handle_users.hash_password(password)
    user = users_models.User(email=email, hashed_password=hashed_password)
    client_connexion = collections_handeler.ClientCollection()
    client_connexion.add_new_user(user)
    return {"message": "User created successfully", "email": email}


@router.post("/login")
async def login(
    response: Response, form_data: OAuth2PasswordRequestForm = Depends()
) -> dict:
    """

    Parameters
    ----------
    response : <class 'starlette.responses.Response'>
    form_data : <class 'fastapi.security.oauth2.OAuth2PasswordRequestForm'>

    Returns
    -------

    """
    client_connexion = collections_handeler.ClientCollection()
    user = client_connexion.read(form_data.username)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not handle_users.verify_password(
            form_data.password,
            user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/logout")
async def logout(response: Response) -> dict:
    """
    logout function
    Parameters
    ----------
    response :

    Returns
    -------

    """
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}


@router.get("/me")
async def read_users_me(
        current_user: dict = Depends(get_current_user)) -> dict:
    """

    Parameters
    ----------
    current_user :

    Returns
    -------

    """
    return {"email": current_user["email"]}
