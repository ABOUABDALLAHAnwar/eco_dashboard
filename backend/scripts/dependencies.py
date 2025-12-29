import jwt
from fastapi import Cookie, HTTPException
from fastapi.security import OAuth2PasswordBearer  # , OAuth2PasswordRequestForm

import backend.scripts.variables as variables
from backend.configs.config import SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
ALGORITHM = variables.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = variables.ACCESS_TOKEN_EXPIRE_MINUTES


def decode_access_token(token: str):
    """

    Parameters
    ----------
    token

    Returns
    -------

    """
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
