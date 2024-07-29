from typing import TYPE_CHECKING, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

from src.common import base_crud as bs
from src.modules.accounts.schemas import AccountCreate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=DeclarativeBase)
D = TypeVar('D', bound=BaseModel)


async def create_account(session: "AsyncSession", model: Type[T], data: D, user_id: int):
    new_data = data.model_dump()
    new_data["user_id"] = user_id
    account_data = AccountCreate(**new_data)
    return await bs.create_item(session=session, model=model, data=account_data)


