from typing import Type, TypeVar, Callable, TYPE_CHECKING
from fastapi import Depends, HTTPException, status, Path
from core.models.database import get_database
from sqlalchemy.orm import DeclarativeBase
from typing import Annotated
from common.base_crud import get_item

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=DeclarativeBase)


# async def get_item_by_id(
#         item_id: Annotated[int, Path],
#         model: Type[T],
#         session: AsyncSession = Depends(get_database().session_dependency)
# ) -> T:
#     item = await get_item(session=session, model=model, item_id=item_id)
#     if item:
#         return item
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail=f"{model.__name__} {item_id} not found!"
#     )


def get_item_by_id(model: Type[T]) -> Callable:
    async def dependency(
        item_id: Annotated[int, Path],
        session: Annotated[AsyncSession, Depends(get_database().session_dependency)]
    ) -> T:
        item = await get_item(session=session, model=model, item_id=item_id)
        if item:
            return item
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} {item_id} not found!"
        )
    return dependency
