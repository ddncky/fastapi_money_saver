from fastapi import APIRouter
from src.api.views import router as account_router



modules_router = APIRouter()
modules_router.include_router(account_router)