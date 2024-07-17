from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import select, Result
from typing import TYPE_CHECKING, TypeVar, Type
from . schemas import CategoryCreate
from src.common import base_crud as bs

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=DeclarativeBase)
D = TypeVar('D', bound=BaseModel)


async def get_base_categories(session: "AsyncSession", model: Type[T]) -> list[T]:
    stmt = select(model).where(model.user_id.is_(None)).order_by(model.id)
    result: Result = await session.execute(stmt)
    categories = result.scalars().all()

    return list(categories)


async def create_category(session: "AsyncSession", model: Type[T], data: D, user_id: int):
    new_data = data.model_dump()
    new_data["user_id"] = user_id
    account_data = CategoryCreate(**new_data)
    return await bs.create_item(session=session, model=model, data=account_data)

