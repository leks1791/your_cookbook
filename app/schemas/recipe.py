from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


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


class PaginatedRecipeResponse(BaseModel):
    items: list[RecipeResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
