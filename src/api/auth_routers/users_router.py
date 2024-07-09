from fastapi import APIRouter
from .fastapi_users_router import fastapi_users
from src.modules.users.schemas import UserRead, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# /me, /{id}
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)