from fastapi import Depends, Path, HTTPException, status
from src.modules import User
from src.api.auth_routers.fastapi_users_router import current_active_user
from sqlalchemy import select, and_, or_
from typing import Annotated, TYPE_CHECKING
from src.core import get_database
from . import Category
from src.common import base_dependencies as bd

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from . models import User


async def get_user_categories_ids(
    session: "AsyncSession" = Depends(get_database().session_dependency),
    current_user: "User" = Depends(current_active_user),
):
    stmt = (select(Category.id).where(or_(Category.user_id == current_user.id, Category.user_id.is_(None))).
            order_by(Category.id))
    result = await session.execute(stmt)
    ids = result.scalars().all()

    return ids


async def is_category_owner_or_superuser(
    category_id: Annotated[int, Path],
    current_user: "User" = Depends(current_active_user),
    session: "AsyncSession" = Depends(get_database().session_dependency),

):
    ids = await get_user_categories_ids(session=session, current_user=current_user)

    if not current_user.is_superuser and category_id not in ids:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource")


async def get_category_and_check_permissions_only_for_getting_ids(
    category_id: Annotated[int, Path],
    session: "AsyncSession" = Depends(get_database().session_dependency),
    current_user: "User" = Depends(current_active_user)
) -> Category:
    """This function and two above were created to be able to retrieve categories created
    by current (not super) user and base categories"""
    await is_category_owner_or_superuser(category_id, current_user, session)
    category = await bd.get_item_by_id(Category)(category_id, session)
    return category


async def get_category_and_check_permissions(
    category_id: Annotated[int, Path],
    session: "AsyncSession" = Depends(get_database().session_dependency),
    current_user: "User" = Depends(current_active_user)
) -> Category:
    await bd.is_item_owner_or_superuser(Category)(category_id, current_user, session)
    category = await bd.get_item_by_id(Category)(category_id, session)
    return category
