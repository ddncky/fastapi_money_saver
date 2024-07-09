from fastapi import APIRouter
from .fastapi_users_router import fastapi_users
from api.dependencies.authentication.backend import authentication_backend


router = APIRouter(prefix="/auth", tags=["Auth"])

router.include_router(
    router=fastapi_users.get_auth_router(authentication_backend)
)
