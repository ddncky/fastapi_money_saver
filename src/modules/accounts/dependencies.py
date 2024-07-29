from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy import select

from src.api.auth_routers.fastapi_users_router import current_active_user
from src.common import base_dependencies as bd
from src.core import get_database
from src.modules import User

from . import Account

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_account_and_check_permissions(
    account_id: Annotated[int, Path],
    session: "AsyncSession" = Depends(get_database().session_dependency),
    current_user: User = Depends(current_active_user)
) -> Account:
    await bd.is_item_owner_or_superuser(Account)(account_id, current_user, session)
    account = await bd.get_item_by_id(Account)(account_id, session)
    return account
