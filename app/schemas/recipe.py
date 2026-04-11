from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RecipeCreate(BaseModel):
    title: str
    description: str | None = None
    ingredients: str


class RecipeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    ingredients: str
    user_id: int
    created_at: datetime | None = None


class PaginatedRecipeResponse(BaseModel):
    items: list[RecipeResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
