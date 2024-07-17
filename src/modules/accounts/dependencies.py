from fastapi import Depends, HTTPException, status, Path
from src.modules import User
from src.api.auth_routers.fastapi_users_router import current_active_user
from typing import Annotated, TYPE_CHECKING
from src.core import get_database
from sqlalchemy import select
from . import Account
from src.common import base_dependencies as bd

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_account_ids(
    session: "AsyncSession" = Depends(get_database().session_dependency),
    current_user: User = Depends(current_active_user),
):
    stmt = select(Account.id).where(current_user.id == Account.user_id)
    result = await session.execute(stmt)
    ids = result.scalars().all()

    return ids


async def is_account_owner_or_superuser(
    account_id: Annotated[int, Path],
    current_user: User = Depends(current_active_user),
    session: "AsyncSession" = Depends(get_database().session_dependency),

):
    ids = await get_user_account_ids(session=session, current_user=current_user)

    if not current_user.is_superuser and account_id not in ids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource")


async def get_account_and_check_permissions(
    account_id: Annotated[int, Path],
    session: "AsyncSession" = Depends(get_database().session_dependency),
    current_user: User = Depends(current_active_user)
) -> Account:
    await is_account_owner_or_superuser(account_id, current_user, session)
    account = await bd.get_item_by_id(Account)(account_id, session)
    return account
