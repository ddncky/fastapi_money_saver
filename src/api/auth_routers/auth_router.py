from fastapi import APIRouter
from .fastapi_users_router import fastapi_users
from api.dependencies.authentication.backend import authentication_backend
from src.modules.users.schemas import UserRead, UserCreate

router = APIRouter(prefix="/auth", tags=["Auth"])


# /login, /logout
router.include_router(
    router=fastapi_users.get_auth_router(authentication_backend)
)

# /register
router.include_router(
    router=fastapi_users.get_register_router(UserRead, UserCreate)
)