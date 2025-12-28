import jwt
from fastapi import (
    Cookie,
    Depends,  # Request,  Response, APIRouter
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer  # , OAuth2PasswordRequestForm

import backend.scripts.variables as variables
from backend.configs.config import SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
ALGORITHM = variables.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = variables.ACCESS_TOKEN_EXPIRE_MINUTES


def get_current_user_oauth2(token: str = Depends(oauth2_scheme)) -> dict:
    """
    function for authorisations, in this function we check if user have authorisation to use a route

    Parameters
    ----------
    token :

    Returns
    -------

    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        user = variables.client_accounts_collection.find_one({"email": email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None


def get_current_user(access_token: str = Cookie(None)):

    if not access_token:
        raise HTTPException(status_code=401, detail="Token manquant")
    try:

        payload = decode_access_token(
            access_token
        )  # fonction que tu utilises pour ton JWT

        email = payload.get("sub")

        if not email:
            raise HTTPException(status_code=401, detail="Token invalide")
        return {"email": email}
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalide")
