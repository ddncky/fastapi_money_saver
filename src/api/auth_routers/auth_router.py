from fastapi import APIRouter

from src.api.dependencies.authentication.backend import authentication_backend
from src.modules.users.schemas import UserCreate, UserRead

from .fastapi_users_router import fastapi_users_inst

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


# /login, /logout
router.include_router(
    router=fastapi_users_inst.get_auth_router(
        authentication_backend,
        requires_verification=False
    )
)

# /register
router.include_router(
    router=fastapi_users_inst.get_register_router(UserRead, UserCreate)
)

# /request-verify-token, /verify
# router.include_router(
#     router=fastapi_users_inst.get_verify_router(UserRead)
# )

# /forgot-password, /reset-password
router.include_router(
    router=fastapi_users_inst.get_reset_password_router()
)
