from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from .auth_routers.auth_router import router as auth_router
from .auth_routers.users_router import router as users_router


http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix="/api",
    dependencies=[Depends(http_bearer)]
)

router.include_router(auth_router)
router.include_router(users_router)

