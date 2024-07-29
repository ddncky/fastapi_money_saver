from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.mixins import IntIdPkMixin
from src.core import Base

if TYPE_CHECKING:
    from src.modules import Transaction, User


class Account(IntIdPkMixin, Base):
    __tablename__ = "accounts"

    name: Mapped[str] = mapped_column(String(100), nullable=True)  # False?
    balance: Mapped[float] = mapped_column(Float, default=0.0)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    users: Mapped["User"] = relationship("User", back_populates="accounts")
    transactions: Mapped[list["Transaction"]] = relationship("Transaction", back_populates="accounts")

    def __str__(self):
        return f"Account #{self.id} {self.name}"
