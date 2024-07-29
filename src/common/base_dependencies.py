from typing import TYPE_CHECKING, Annotated, Callable, Type, TypeVar

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase

from src.api.auth_routers.fastapi_users_router import current_active_user
from src.common.base_crud import get_item
from src.core.models.database import get_database

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.modules import User

T = TypeVar("T", bound=DeclarativeBase)


def get_item_by_id(model: Type[T]) -> Callable:
    async def dependency(
            item_id: Annotated[int, Path],
            session: Annotated["AsyncSession", Depends(get_database().session_dependency)]
    ) -> T:
        item = await get_item(session=session, model=model, item_id=item_id)
        if item:
            return item
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} {item_id} not found!"
        )

    return dependency


async def get_user_item_ids(
        model: Type[T],
        session: "AsyncSession" = Depends(get_database().session_dependency),
        current_user: "User" = Depends(current_active_user),
):
    stmt = select(model.id).where(current_user.id == model.user_id)
    result = await session.execute(stmt)
    ids = result.scalars().all()

    return ids


def is_item_owner_or_superuser(model: Type[T]):
    async def dependency(
            item_id: Annotated[int, Path],
            current_user: "User" = Depends(current_active_user),
            session: "AsyncSession" = Depends(get_database().session_dependency),
    ):
        ids = await get_user_item_ids(session=session, current_user=current_user, model=model)

        if not current_user.is_superuser and item_id not in ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this resource")
    return dependency


