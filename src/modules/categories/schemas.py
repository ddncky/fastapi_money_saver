from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    name: str


class CategoryCreateInput(CategoryBase):
    pass


class CategoryCreate(CategoryBase):
    user_id: int


class CategoryUpdate(CategoryBase):
    pass


class CategoryUpdatePartially(CategoryBase):
    name: str | None = None


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None
