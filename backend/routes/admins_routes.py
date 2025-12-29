from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from backend.configs import config
from backend.database import collections_handeler
from backend.models import users_models
from backend.users_handler import handle_users

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------

router = APIRouter(tags=["Admins"])


@router.delete("/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(request: Request, email: str):
    """

    Parameters
    ----------
    request
    email

    Returns
    -------

    """
    clients_collectons = collections_handeler.ClientCollection()
    collections_handeler.UserProfileInfos()
    collections_handeler.ClientActions()

    return Response(status_code=status.HTTP_204_NO_CONTENT)