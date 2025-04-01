import sys
from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from pathlib import Path

sys.path.append(
    str(Path(__file__).parent.parent.parent)
)
from app.user.auth import get_user_manager, auth_backend
from app.models import User
from app.user.schemas import UserRead, UserCreate, UserUpdate


router = APIRouter()


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)


router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)


router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
