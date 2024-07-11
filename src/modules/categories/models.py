from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String

from src.common.mixins import IntIdPkMixin
from src.core import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.modules import Transaction


class Category(IntIdPkMixin, Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    transactions: Mapped[list["Transaction"]] = relationship("Transaction", back_populates="categories")