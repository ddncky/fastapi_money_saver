from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, DateTime, Float, ForeignKey
from src.core import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.modules import User
    from src.modules import Transaction


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)  # False?
    balance: Mapped[float] = mapped_column(Float, default=0.0)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    users: Mapped["User"] = relationship("User", back_populates="accounts")
    transactions: Mapped[list["Transaction"]] = relationship("Transaction", back_populates="accounts")