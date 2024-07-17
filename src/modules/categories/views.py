from fastapi import APIRouter, Depends, status

from src.api.auth_routers.fastapi_users_router import current_active_user, current_active_superuser
from .schemas import (
    CategoryUpdate,
    CategoryUpdatePartially,
    CategoryRead,
    CategoryCreateInput)
from .models import Category
from src.core import get_database
from src.common import base_crud as bs
from typing import Optional, Annotated, TYPE_CHECKING
from src.common import base_dependencies as bd
from src.common import base_crud as bc
from . import crud
from . dependencies import (
    get_category_and_check_permissions_only_for_getting_ids,
    get_category_and_check_permissions
)
if TYPE_CHECKING:
    from src.modules import User
    from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
        category_in: CategoryCreateInput,
        user: Annotated["User", Depends(current_active_user)],
        session: "AsyncSession" = Depends(get_database().session_dependency),
):
    return await crud.create_category(session=session, model=Category, data=category_in, user_id=user.id)


@router.get("/", response_model=list[CategoryRead], dependencies=[Depends(current_active_superuser)])
async def get_categories(
        session: "AsyncSession" = Depends(get_database().session_dependency)
):
    return await bs.get_items(session=session, model=Category)


@router.get("/base/", response_model=list[CategoryRead])
async def get_base_categories(
        session: "AsyncSession" = Depends(get_database().session_dependency)
):
    return await crud.get_base_categories(session=session, model=Category)


@router.get("/me/", response_model=list[CategoryRead])
async def get_user_accounts(
        user: Annotated["User", Depends(current_active_user)],
        session: Annotated["AsyncSession", Depends(get_database().session_dependency)],
):
    return await bc.get_items_by_current_user(session=session, model=Category, user_id=user.id)


@router.get(
    "/{category_id}/",
    response_model=Optional[CategoryRead],
    description="If not superuser: Able to retrieve base categories and created by the current user"
)
async def get_caterogy(
        category: Category = Depends(get_category_and_check_permissions_only_for_getting_ids),
):
    return category


@router.put("/{category_id}/", response_model=CategoryRead)
async def update_category(
        category_update: CategoryUpdate,
        category: Category = Depends(get_category_and_check_permissions),
        session: "AsyncSession" = Depends(get_database().session_dependency)
):
    return await bs.update_item(
        session=session,
        item=category,
        data=category_update
    )


@router.patch("/{category_id}/", response_model=CategoryRead)
async def update_category_partially(
        category_update: CategoryUpdatePartially,
        category: Category = Depends(get_category_and_check_permissions),
        session: "AsyncSession" = Depends(get_database().session_dependency),
        partial: bool = True
):
    return await bs.update_item(
        session=session,
        item=category,
        data=category_update,
        partial=partial
    )


@router.delete("/{category_id}/")
async def delete_category(
        category: Category = Depends(get_category_and_check_permissions),
        session: "AsyncSession" = Depends(get_database().session_dependency)
) -> None:
    await bs.delete_item(session=session, item=category)
