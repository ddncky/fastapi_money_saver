from pydantic import BaseModel, ConfigDict
from datetime import datetime


class AccountBase(BaseModel):
    name: str
    balance: float


class AccountCreate(AccountBase):
    pass


class AccountUpdate(AccountBase):
    pass


class AccountUpdatePartially(AccountBase):
    name: str | None = None
    balance: float | None = None


class AccountRead(AccountBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


