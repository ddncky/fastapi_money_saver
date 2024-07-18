from pydantic import BaseModel, ConfigDict
from datetime import datetime
from .models import TransactionType


class TransactionBase(BaseModel):
    amount: float
    description: str
    date: datetime
    type: TransactionType
    account_id: int
    category_id: int


class TransactionCreateInput(BaseModel):
    amount: float
    description: str
    date: datetime
    type: TransactionType


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):  # TODO: do full update with all fields;
    description: str
    date: datetime


class TransactionUpdatePartially(TransactionUpdate):
    #amount: float | None = None
    description: str | None = None
    date: datetime | None = None
    #type: #TransactionType | None = None
    #account_id: int | None = None
    #category_id: int | None = None


class TransactionRead(TransactionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    