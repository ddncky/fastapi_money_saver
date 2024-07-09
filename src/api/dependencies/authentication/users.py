from typing import TYPE_CHECKING, Annotated
from fastapi import Depends
from src.core import get_database
from src.modules import User

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_users_db(
    session: Annotated["AsyncSession", Depends(get_database().session_dependency)]
):
    yield User.get_db(session=session)
