import jwt
from fastapi import Depends, HTTPException, status  # Request,  Response, APIRouter
from fastapi.security import OAuth2PasswordBearer  # , OAuth2PasswordRequestForm

import backend.variables as variables
from backend.configs.config import SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


ALGORITHM = variables.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = variables.ACCESS_TOKEN_EXPIRE_MINUTES


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
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
