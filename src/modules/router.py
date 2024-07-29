from fastapi import APIRouter

from .accounts.views import router as account_router
from .categories.views import router as categories_router
from .transactions.views import router as transactions_router

modules_router = APIRouter()
modules_router.include_router(account_router)
modules_router.include_router(categories_router)
modules_router.include_router(transactions_router)
