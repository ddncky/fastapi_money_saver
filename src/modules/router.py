from fastapi import APIRouter
from src.modules.accounts.views import router as account_router



modules_router = APIRouter()
modules_router.include_router(account_router)