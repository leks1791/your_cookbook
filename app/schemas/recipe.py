from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class RecipeIngredient(BaseModel):
    name: str
    amount: str | None = None
    unit: str | None = None


class RecipeStep(BaseModel):
    order: int
    description: str
    timer_seconds: int | None = None


class RecipeCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    ingredients: str  # JSON string or comma-separated
    steps: str | None = None  # JSON string
    tags: list[str] | None = None
    photos: list[str] | None = None
    prep_time: int | None = Field(None, ge=0)
    cook_time: int | None = Field(None, ge=0)
    servings: int | None = Field(None, ge=1)
    difficulty: str | None = None  # easy, medium, hard
    cuisine: str | None = None
    notes: str | None = None
    category_ids: list[int] | None = Field(
        default=None, description="ID категорий для рецепта"
    )


class RecipeUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    ingredients: str | None = None
    steps: str | None = None
    tags: list[str] | None = None
    photos: list[str] | None = None
    prep_time: int | None = Field(None, ge=0)
    cook_time: int | None = Field(None, ge=0)
    servings: int | None = Field(None, ge=1)
    difficulty: str | None = None
    cuisine: str | None = None
    notes: str | None = None
    category_ids: list[int] | None = Field(None, description="ID категорий для рецепта")


class RecipeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    ingredients: str
    steps: str | None = None
    tags: list[str] | None = None
    photos: list[str] | None = None
    prep_time: int | None = None
    cook_time: int | None = None
    servings: int | None = None
    difficulty: str | None = None
    cuisine: str | None = None
    notes: str | None = None
    user_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    categories: list[dict] | None = None  # Список категорий с id и name

    @field_serializer("categories")
    def serialize_categories(self, categories):
        if categories is None:
            return []
        return [
            {"id": cat.id, "name": cat.name, "color": cat.color} for cat in categories
        ]


class PaginatedRecipeResponse(BaseModel):
    items: list[RecipeResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
