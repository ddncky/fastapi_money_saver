from src.core import get_database
from src.modules.categories import Category
from src.modules.categories.schemas import CategoryCreate
from src.common.base_crud import create_item
import asyncio


def base_categories():
    categories = [
        {"name": "Зарплата"},
        {"name": "Аванс"},
        {"name": "Возврат долга"},
        {"name": "Неожиданная находка"},
        {"name": "Подработка"},
        {"name": "Процент с вложений"},
    ]
    return categories


async def create_basic_categories():
    async with get_database().session_factory() as session:
        categories = base_categories()
        for category in categories:
            data = CategoryCreate(**category)
            await create_item(session=session, model=Category, data=data)


if __name__ == "__main__":
    asyncio.run(create_basic_categories())
