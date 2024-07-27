from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey

from src.common.mixins import IntIdPkMixin
from src.core import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.modules import Transaction
    from src.modules import User


class Category(IntIdPkMixin, Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)

    transactions: Mapped[list["Transaction"]] = relationship("Transaction", back_populates="categories")
    users: Mapped["User"] = relationship("User", back_populates="categories")

    def __str__(self):
        return f"Category #{self.id} {self.name}"