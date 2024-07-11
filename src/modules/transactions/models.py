from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, Float, String, DateTime, ForeignKey, Enum
from datetime import datetime

from src.common.mixins import IntIdPkMixin
from src.core import Base
import enum
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.modules import Account
    from src.modules import Category


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