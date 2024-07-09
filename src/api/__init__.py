from fastapi import APIRouter
from .auth_routers.auth_router import router as auth_router
from .auth_routers.users_router import router as users_router

router = APIRouter(prefix="/api")
router.include_router(auth_router)
router.include_router(users_router)

