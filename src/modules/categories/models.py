from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.mixins import IntIdPkMixin
from src.core import Base

if TYPE_CHECKING:
    from src.modules import Transaction, User


class Category(IntIdPkMixin, Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)

    transactions: Mapped[list["Transaction"]] = relationship("Transaction", back_populates="categories")
    users: Mapped["User"] = relationship("User", back_populates="categories")

    def __str__(self):
        return f"Category #{self.id} {self.name}"