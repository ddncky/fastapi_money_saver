from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from src.core.base import Base
from src.common.mixins.int_id_pk import IntIdPkMixin


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[int]):
    pass
