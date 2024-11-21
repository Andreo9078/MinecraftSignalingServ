import uuid

from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin, FastAPIUsers

from src.config import SECRET_KEY
from .backends import get_jwt_strategy, auth_backend
from .models import User, get_user_db


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET_KEY
    verification_token_secret = SECRET_KEY


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
current_user = fastapi_users.current_user()
