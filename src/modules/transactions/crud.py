from typing import TYPE_CHECKING, TypeVar, Sequence

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, joinedload

from src.common import base_crud as bc
from src.modules.accounts.models import Account
from src.modules.categories import Category

from .models import Transaction, TransactionType
from .schemas import TransactionCreate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=DeclarativeBase)
D = TypeVar("D", bound=BaseModel)


async def create_transaction(
    session: "AsyncSession",
    data,
    account: Account,
    category: Category,
):  # TODO: transaction transfer;
    new_data = data.model_dump()
    new_data["account_id"] = account.id
    new_data["category_id"] = category.id
    transaction_data = TransactionCreate(**new_data)
    transaction = await bc.create_item(
        session=session, model=Transaction, data=transaction_data
    )

    if data.type == TransactionType.income:
        account.balance += data.amount
    else:
        account.balance -= data.amount

    await session.commit()
    return transaction


async def get_user_transactions(session: "AsyncSession", user_id: int) -> Sequence[Transaction]:
    stmt = (
        select(Transaction)
        .join(Account, Account.id == Transaction.account_id)
        .options(joinedload(Transaction.accounts))
        .where(Account.user_id == user_id)
        .order_by(Transaction.id.desc())
    )
    result = await session.execute(stmt)
    transactions = result.scalars().all()
    return transactions


