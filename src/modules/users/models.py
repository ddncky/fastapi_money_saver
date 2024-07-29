import datetime
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.generics import TIMESTAMPAware, now_utc
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.mixins import IntIdPkMixin
from src.core import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.modules import Account, Category


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[int]):
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMPAware(timezone=True), index=True, nullable=False, default=now_utc
    )

    accounts: Mapped[list["Account"]] = relationship("Account", back_populates="users")
    categories: Mapped[list["Category"]] = relationship("Category", back_populates="users")

    def __str__(self):
        return f"User #{self.id} {self.email}"

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, User)

