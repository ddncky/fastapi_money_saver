from fastapi import APIRouter
from .auth_routers.auth_router import router as auth_router

router = APIRouter(prefix="/api", tags=["Auth"])  # TODO: api or auth?
router.include_router(auth_router)

