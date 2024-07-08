from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from src.core import Base
from src.common.mixins import IntIdPkMixin
from typing import TYPE_CHECKING

# TODO: переименовать этот файл в модель или переместить его потом;

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[int]):

    @classmethod
    def get_users_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, User)

