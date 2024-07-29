from typing import TYPE_CHECKING, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import Result, select
from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar("T", bound=DeclarativeBase)
D = TypeVar('D', bound=BaseModel)


async def create_item(session: "AsyncSession", model: Type[T], data: D) -> T:
    item = model(**data.model_dump())
    session.add(item)
    await session.commit()

    return item


async def get_items_by_current_user(session: "AsyncSession", model: Type[T], user_id: int) -> list[T]:
    stmt = select(model).where(model.user_id == user_id)
    result: Result = await session.execute(stmt)
    items = result.scalars().all()

    return list(items)


async def get_item(session: "AsyncSession", model: Type[T], item_id: int) -> T | None:
    return await session.get(model, item_id)


async def get_items(session: "AsyncSession", model: Type[T]) -> list[T]:
    stmt = select(model).order_by(model.id)
    result: Result = await session.execute(stmt)
    items = result.scalars().all()

    return list(items)


async def update_item(
        session: "AsyncSession",
        item: T,
        data: D,
        partial: bool = False
) -> T:
    for name, value in data.model_dump(exclude_unset=partial).items():
        setattr(item, name, value)
    await session.commit()

    return item


async def delete_item(session: "AsyncSession", item: T) -> None:
    await session.delete(item)
    await session.commit()
