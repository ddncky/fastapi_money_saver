from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.auth_routers.fastapi_users_router import (
    current_active_superuser,
    current_active_user,
)
from src.modules import User
from src.modules.users.schemas import UserRead

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.get("")
def get_user_messages(
    user: Annotated[
        User,
        Depends(current_active_user),
    ],
):
    return {
        "messages": ["m1", "m2", "m3"],
        "user": UserRead.model_validate(user),
    }


@router.get("/secrets")
def get_superuser_messages(
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
):
    return {
        "messages": ["secret-m1", "secret-m2", "secret-m3"],
        "user": UserRead.model_validate(user),
    }