from fastapi import APIRouter

from src.modules.users.schemas import UserRead, UserUpdate

from .fastapi_users_router import fastapi_users_inst

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# /me, /{id}
router.include_router(
    fastapi_users_inst.get_users_router(UserRead, UserUpdate),
)
