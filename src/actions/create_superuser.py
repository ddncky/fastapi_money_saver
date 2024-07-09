import asyncio
import contextlib
import logging

from src.core import get_database
from src.modules.users.schemas import UserCreate
from src.api.dependencies.authentication.user_manager import get_user_manager
from src.core.authentication.user_manager import UserManager
from src.api.dependencies.authentication.users import get_users_db
from typing import TYPE_CHECKING
from src.core import get_settings

log = logging.getLogger(__name__)


if TYPE_CHECKING:
    from src.modules import User

get_users_db_context = contextlib.asynccontextmanager(get_users_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    user_manager: UserManager,
    user_create: UserCreate,
) -> "User":
    user = await user_manager.create(
        user_create=user_create,
        safe=False
    )
    log.warning("User %r has been created.", user.email)
    return user


async def create_superuser():
    user_create = UserCreate(
        email=get_settings().default_superuser_email,
        password=get_settings().default_superuser_password,
        is_active=get_settings().default_superuser_is_active,
        is_superuser=get_settings().default_superuser_is_superuser,
        is_verified=get_settings().default_superuser_is_verified,

    )
    async with get_database().session_factory() as session:
        async with get_users_db_context(session) as users_db:
            async with get_user_manager_context(users_db) as user_manager:
                return await create_user(
                    user_manager=user_manager,
                    user_create=user_create
                )


if __name__ == "__main__":
    asyncio.run(create_superuser())
