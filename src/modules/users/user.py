import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.generics import TIMESTAMPAware, now_utc
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core import Base
from src.common.mixins import IntIdPkMixin
from typing import TYPE_CHECKING

# TODO: переименовать этот файл в модель или переместить его потом;


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from src.modules import Account


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[int]):
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMPAware(timezone=True), index=True, nullable=False, default=now_utc
    )

    accounts: Mapped[list["Account"]] = relationship("Account", back_populates="users")

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, User)

