import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.mixins import IntIdPkMixin
from src.core import Base

if TYPE_CHECKING:
    from src.modules import Account, Category


class TransactionType(enum.Enum):
    income = "income"
    expense = "expense"


class Transaction(IntIdPkMixin, Base):
    __tablename__ = "transactions"

    amount: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(100))
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType), nullable=False)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"))
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))

    accounts: Mapped["Account"] = relationship("Account", back_populates="transactions")
    categories: Mapped["Category"] = relationship("Category", back_populates="transactions")

    def __str__(self):
        return f"Transaction #{self.id}"
