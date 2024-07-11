import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime

from src.core import Base
from src.common.mixins import IntIdPkMixin
from typing import TYPE_CHECKING

# TODO: переименовать этот файл в модель или переместить его потом;

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.modules import Account


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[int]):
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.now(datetime.UTC))

    accounts: Mapped[list["Account"]] = relationship("Account", back_populates="users")

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, User)

