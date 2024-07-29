from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from src.core import AccessToken, get_database

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_token_db(
    session: Annotated["AsyncSession", Depends(get_database().session_dependency)]
):
    yield AccessToken.get_db(session=session)