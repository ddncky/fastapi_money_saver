from typing import TYPE_CHECKING, Annotated, Optional

from fastapi import APIRouter, Depends, status

import src.modules.transactions.crud as crud
from src.api.auth_routers.fastapi_users_router import (
    current_active_superuser,
    current_active_user,
)
from src.common import base_crud as bc
from src.core import get_database
from src.modules.accounts.dependencies import get_account_and_check_permissions
from src.modules.categories.dependencies import (
    get_category_and_check_permissions_only_for_getting_ids,
)

from .dependencies import get_transaction_and_check_permissions
from .models import Transaction
from .schemas import (
    TransactionCreateInput,
    TransactionRead,
    TransactionUpdate,
    TransactionUpdatePartially,
)
from fastapi_cache.decorator import cache

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.modules import Account, Category, User

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/transactions/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_in: TransactionCreateInput,
    account: "Account" = Depends(get_account_and_check_permissions),
    category: "Category" = Depends(get_category_and_check_permissions_only_for_getting_ids),
    session: "AsyncSession" = Depends(get_database().session_dependency)
) -> TransactionRead:
    transaction = await crud.create_transaction(
        session=session,
        data=transaction_in,
        account=account,
        category=category
    )
    return transaction


@router.get("/", response_model=list[TransactionRead], dependencies=[Depends(current_active_superuser)])
async def get_transactions(
        session: "AsyncSession" = Depends(get_database().session_dependency)
):
    return await bc.get_items(session=session, model=Transaction)


@router.get("/me/", response_model=list[TransactionRead])
@cache(expire=30)
async def get_user_transactions(
        user: Annotated["User", Depends(current_active_user)],
        session: Annotated["AsyncSession", Depends(get_database().session_dependency)],
):
    return await crud.get_user_transactions(session=session, user_id=user.id)


@router.get("/{transaction_id}/", response_model=Optional[TransactionRead])
async def get_transaction(
        transaction: Transaction = Depends(get_transaction_and_check_permissions)
):
    return transaction


@router.put("/{transaction_id}/", response_model=TransactionRead)
async def update_transaction(
        transaction_update: TransactionUpdate,
        transaction: Transaction = Depends(get_transaction_and_check_permissions),
        session: "AsyncSession" = Depends(get_database().session_dependency)
):
    return await bc.update_item(
        session=session,
        item=transaction,
        data=transaction_update
    )


@router.patch("/{transaction_id}/", response_model=TransactionRead)
async def update_transaction_partially(
        transaction_update: TransactionUpdatePartially,
        transaction: Transaction = Depends(get_transaction_and_check_permissions),
        session: "AsyncSession" = Depends(get_database().session_dependency),
        partial: bool = True
):
    return await bc.update_item(
        session=session,
        item=transaction,
        data=transaction_update,
        partial=partial
    )


@router.delete("/{transaction_id}/")
async def delete_transaction(
        transaction: Transaction = Depends(get_transaction_and_check_permissions),
        session: "AsyncSession" = Depends(get_database().session_dependency)
) -> None:
    await bc.delete_item(session=session, item=transaction)
