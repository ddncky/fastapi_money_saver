from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from core.models.base import Base
from src.common.mixins.int_id_pk import IntIdPkMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[int]):

    @classmethod
    def get_users_db(cls, session: AsyncSession):
        return SQLAlchemyUserDatabase(session, User)
