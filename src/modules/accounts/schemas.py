from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AccountBase(BaseModel):
    name: str
    balance: float


class AccountCreateInput(AccountBase):
    pass


class AccountCreate(AccountBase):
    user_id: int


class AccountUpdate(AccountBase):
    pass


class AccountUpdatePartially(AccountBase):
    name: str | None = None
    balance: float | None = None


class AccountRead(AccountBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


