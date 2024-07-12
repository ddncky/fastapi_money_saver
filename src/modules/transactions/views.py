from fastapi import APIRouter, Depends, status
from .schemas import TransactionCreate, TransactionUpdate, TransactionUpdatePartially, TransactionRead
from .models import Transaction
from src.core import get_database
from sqlalchemy.ext.asyncio import AsyncSession
from src.common import base_crud as bs
from typing import Optional
from src.common import base_dependencies as bd


router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(
        transaction_in: TransactionCreate,
        session: AsyncSession = Depends(get_database().session_dependency),
):
    return await bs.create_item(session=session, model=Transaction, data=transaction_in)


@router.get("/", response_model=list[TransactionRead])
async def get_transactions(
        session: AsyncSession = Depends(get_database().session_dependency)
):
    return await bs.get_items(session=session, model=Transaction)


@router.get("/{transaction_id}/", response_model=Optional[TransactionRead])
async def get_transaction(
        transaction: Transaction = Depends(bd.get_item_by_id(Transaction)),
):
    return transaction


@router.put("/{transaction_id}/", response_model=TransactionRead)
async def update_transaction(
        transaction_update: TransactionUpdate,
        transaction: Transaction = Depends(bd.get_item_by_id(Transaction)),
        session: AsyncSession = Depends(get_database().session_dependency)
):
    return await bs.update_item(
        session=session,
        item=transaction,
        data=transaction_update
    )


@router.patch("/{transaction_id}/", response_model=TransactionRead)
async def update_transaction_partially(
        transaction_update: TransactionUpdatePartially,
        transaction: Transaction = Depends(bd.get_item_by_id(Transaction)),
        session: AsyncSession = Depends(get_database().session_dependency),
        partial: bool = True
):
    return await bs.update_item(
        session=session,
        item=transaction,
        data=transaction_update,
        partual=partial
    )


@router.delete("/{transaction_id}/")
async def delete_transaction(
        transaction: Transaction = Depends(bd.get_item_by_id(Transaction)),
        session: AsyncSession = Depends(get_database().session_dependency)
) -> None:
    await bs.delete_item(session=session, item=transaction)
