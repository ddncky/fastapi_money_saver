from asyncio import current_task
from functools import lru_cache
from typing import Iterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from src.core.config import get_settings


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> Iterator[AsyncSession]:
        # async with self.session_factory() as session:  Так тоже можно;
        #     try:
        #         yield session
        #     finally:
        #         await session.close()
        session = self.get_scoped_session()
        try:
            yield session
        finally:
            await session.remove()


@lru_cache
def get_database() -> DatabaseHelper:
    db_helper = DatabaseHelper(
        url=get_settings().db_url,
        echo=get_settings().DB_ECHO
    )
    return db_helper

