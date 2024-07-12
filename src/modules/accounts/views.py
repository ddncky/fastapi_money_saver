import logging
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth_routers.fastapi_users_router import (
    current_active_superuser,
    current_active_user,
)
from src.common import base_crud as bs
from src.common import base_dependencies as bd
from src.core import get_database
from src.modules import User
from src.modules.accounts import crud
from src.modules.accounts.models import Account
from src.modules.accounts.schemas import (
    AccountCreateInput,
    AccountRead,
    AccountUpdate,
    AccountUpdatePartially,
)

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/", response_model=AccountRead, status_code=status.HTTP_201_CREATED)
async def create_account(
        account_in: AccountCreateInput,
        user: Annotated[User, Depends(current_active_superuser)],
        session: AsyncSession = Depends(get_database().session_dependency),
):
    return await crud.create_account(session=session, model=Account, data=account_in, user_id=user.id)


@router.get("/", response_model=list[AccountRead])
async def get_accounts(
        session: AsyncSession = Depends(get_database().session_dependency)
):
    return await bs.get_items(session=session, model=Account)


@router.get("/{account_id}/", response_model=Optional[AccountRead])
async def get_account(
        account: Account = Depends(bd.get_item_by_id(Account)),
):
    return account


@router.put("/{account_id}/", response_model=AccountRead)
async def update_account(
        account_update: AccountUpdate,
        account: Account = Depends(bd.get_item_by_id(Account)),
        session: AsyncSession = Depends(get_database().session_dependency)
):
    return await bs.update_item(
        session=session,
        item=account,
        data=account_update
    )


@router.patch("/{account_id}/", response_model=AccountRead)
async def update_account_partially(
        account_update: AccountUpdatePartially,
        account: Account = Depends(bd.get_item_by_id(Account)),
        session: AsyncSession = Depends(get_database().session_dependency),
        partial: bool = True
):
    return await bs.update_item(
        session=session,
        item=account,
        data=account_update,
        partual=partial
    )


@router.delete("/{account_id}/")
async def delete_account(
        account: Account = Depends(bd.get_item_by_id(Account)),
        session: AsyncSession = Depends(get_database().session_dependency)
) -> None:
    await bs.delete_item(session=session, item=account)







