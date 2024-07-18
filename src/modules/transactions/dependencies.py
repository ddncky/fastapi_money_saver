from fastapi import Depends, Path, HTTPException, status
from src.api.auth_routers.fastapi_users_router import current_active_user
from sqlalchemy import select
from typing import Annotated, TYPE_CHECKING
from src.core import get_database
from . import Transaction
from src.modules import Account
from src.common import base_dependencies as bd

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.modules import User


async def get_user_transactions_ids(
        session: "AsyncSession" = Depends(get_database().session_dependency),
        current_user: "User" = Depends(current_active_user),
):
    stmt = (
        select(Transaction.id)
        .join(Account, Account.id == Transaction.account_id)
        .where(Account.user_id == current_user.id)
        .order_by(Transaction.id.desc())
    )
    result = await session.execute(stmt)
    ids = result.scalars().all()

    return ids


async def is_transaction_owner_or_superuser(
        transaction_id: Annotated[int, Path],
        current_user: "User" = Depends(current_active_user),
        session: "AsyncSession" = Depends(get_database().session_dependency)
):
    ids = await get_user_transactions_ids(session=session, current_user=current_user)

    if not current_user.is_superuser and transaction_id not in ids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource")


async def get_transaction_and_check_permissions(
        transaction_id: Annotated[int, Path],
        session: "AsyncSession" = Depends(get_database().session_dependency),
        current_user: "User" = Depends(current_active_user)
) -> Transaction:
    await is_transaction_owner_or_superuser(transaction_id, current_user, session)
    category = await bd.get_item_by_id(Transaction)(transaction_id, session)
    return category
