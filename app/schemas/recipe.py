import json
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator


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
    ingredients: str
    steps: str | None = None
    tags: list[str] | None = None
    photos: list[str] | None = None
    prep_time: int | None = Field(None, ge=0)
    cook_time: int | None = Field(None, ge=0)
    servings: int | None = Field(None, ge=1)
    difficulty: str | None = None
    cuisine: str | None = None
    notes: str | None = None
    category_ids: list[int] | None = None


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
    category_ids: list[int] | None = None


class AdminRecipeCreate(RecipeCreate):
    visibility: str = "public"


class ReviewRejectionRequest(BaseModel):
    reason: str = Field(..., min_length=3, max_length=1000)


class RecipeStatusResponse(BaseModel):
    id: int
    visibility: str
    publication_status: str
    rejection_reason: str | None = None
    approved_at: datetime | None = None


def parse_json_list(value):
    if value is None:
        return None
    if isinstance(value, list):
        return value
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return None


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
    visibility: str
    publication_status: str
    is_admin_recipe: bool
    approved_by: int | None = None
    approved_at: datetime | None = None
    rejection_reason: str | None = None
    original_recipe_id: int | None = None
    user_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    categories: list[dict] | None = None

    @field_validator("tags", mode="before")
    @classmethod
    def validate_tags(cls, value):
        return parse_json_list(value)

    @field_validator("photos", mode="before")
    @classmethod
    def validate_photos(cls, value):
        return parse_json_list(value)

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
