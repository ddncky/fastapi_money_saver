from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Integer, String
from src.core import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.modules import Transaction


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    transactions: Mapped[list["Transaction"]] = relationship("Transaction", back_populates="categories")