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


@router.delete("/delete_account", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(request: Request, email: str):
    """

    Parameters
    ----------
    request
    email

    Returns
    -------

    """
    clients_collections = collections_handeler.ClientCollection()
    user_profile_infos = collections_handeler.UserProfileInfos()
    client_actions = collections_handeler.ClientActions()
    data = clients_collections.read(email)
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        profile = user_profile_infos.read(email)
        actions = client_actions.read(email)
        if profile:
            user_profile_infos.delete(email)
        if actions:
            client_actions.delete(email)
        clients_collections.delete(email)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
