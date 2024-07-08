from sqlalchemy import select, Result
from sqlalchemy.orm import DeclarativeBase
from typing import TypeVar, Type, TYPE_CHECKING
from pydantic import BaseModel


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar("T", bound=DeclarativeBase)  # ?
D = TypeVar('D', bound=BaseModel)  # ?


async def create_item(session: "AsyncSession", model: Type[T], data: D) -> T:
    item = model(**data.model_dump())
    session.add(item)
    await session.commit()

    return item


async def get_item(session: AsyncSession, model: Type[T], item_id: int) -> T | None:
    return await session.get(model, item_id)


async def get_items(session: AsyncSession, model: Type[T]) -> list[T]:
    stmt = select(model).order_by(model.id)
    result: Result = await session.execute(stmt)
    items = result.scalars().all()

    return list(items)


async def update_item(
        session: AsyncSession,
        item: T,
        data: D,
        partial: bool = False
) -> T:
    for name, value in data.model_dump(exclude_unset=partial).items():
        setattr(item, name, value)
    await session.commit()

    return item


async def delete_item(session: AsyncSession, item: T) -> None:
    await session.delete(item)
    await session.commit()
