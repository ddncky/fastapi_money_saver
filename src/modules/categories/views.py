from fastapi import APIRouter, Depends, status
from .schemas import CategoryCreate, CategoryUpdate, CategoryUpdatePartially, CategoryRead
from .models import Category
from src.core import get_database
from sqlalchemy.ext.asyncio import AsyncSession
from src.common import base_crud as bs
from typing import Optional
from src.common import base_dependencies as bd


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(
        category_in: CategoryCreate,
        session: AsyncSession = Depends(get_database().session_dependency),
):
    return await bs.create_item(session=session, model=Category, data=category_in)


@router.get("/", response_model=list[CategoryRead])
async def get_categories(
        session: AsyncSession = Depends(get_database().session_dependency)
):
    return await bs.get_items(session=session, model=Category)


@router.get("/{category_id}/", response_model=Optional[CategoryRead])
async def get_caterogy(
        category: Category = Depends(bd.get_item_by_id(Category)),
):
    return category


@router.put("/{category_id}/", response_model=CategoryRead)
async def update_category(
        category_update: CategoryUpdate,
        category: Category = Depends(bd.get_item_by_id(Category)),
        session: AsyncSession = Depends(get_database().session_dependency)
):
    return await bs.update_item(
        session=session,
        item=category,
        data=category_update
    )


@router.patch("/{category_id}/", response_model=CategoryRead)
async def update_category_partially(
        category_update: CategoryUpdatePartially,
        category: Category = Depends(bd.get_item_by_id(Category)),
        session: AsyncSession = Depends(get_database().session_dependency),
        partial: bool = True
):
    return await bs.update_item(
        session=session,
        item=category,
        data=category_update,
        partual=partial
    )


@router.delete("/{category_id}/")
async def delete_category(
        category: Category = Depends(bd.get_item_by_id(Category)),
        session: AsyncSession = Depends(get_database().session_dependency)
) -> None:
    await bs.delete_item(session=session, item=category)
