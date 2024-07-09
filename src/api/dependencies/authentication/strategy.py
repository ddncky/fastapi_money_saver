from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from fastapi_users.authentication.strategy.db import DatabaseStrategy

from src.core import get_settings

from .access_tokens import get_access_token_db

if TYPE_CHECKING:
    from fastapi_users.authentication.strategy.db import AccessTokenDatabase

    from src.core import AccessToken


def get_database_strategy(
    access_token_db: Annotated["AccessTokenDatabase[AccessToken]", Depends(get_access_token_db)],
) -> DatabaseStrategy:
    return DatabaseStrategy(
        database=access_token_db,
        lifetime_seconds=get_settings().access_token_lifetime_seconds # TODO: скрипт для переодической отчистки базы
    )
