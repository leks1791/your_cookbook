import re

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, field_validator
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.category import Category
from app.models.recipe import Recipe
from app.models.user import User

router = APIRouter(prefix="/categories", tags=["categories"])


class CategoryCreate(BaseModel):
    name: str
    description: str | None = None
    color: str = "#f97316"

    @field_validator("color")
    @classmethod
    def validate_color(cls, v: str) -> str:
        # Validate HEX color code
        if not re.match(r"^#[0-9A-Fa-f]{6}$", v):
            raise ValueError("Color must be a valid HEX color code (e.g., #f97316)")
        return v.upper()


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None
    color: str
    recipe_count: int = 0

    class Config:
        from_attributes = True


@router.get("", response_model=list[CategoryResponse])
def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # DEBUG: temporarily return all categories across users to verify data visibility
    categories = (
        db.query(Category)
        .filter(Category.user_id == current_user.id)
        .outerjoin(Category.recipes)
        .group_by(Category.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    # Получаем количество рецептов для каждой категории
    result = []
    for cat in categories:
        recipe_count = (
            db.query(Recipe).join(Recipe.categories).filter(Category.id == cat.id)
        ).count()
        result.append(
            CategoryResponse(
                id=cat.id,
                name=cat.name,
                description=cat.description,
                color=cat.color,
                recipe_count=recipe_count,
            )
        )

    return result


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Проверка на дубликат
    existing = (
        db.query(Category)
        .filter(Category.name == category.name, Category.user_id == current_user.id)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Категория с таким названием уже существует",
        )

    db_category = Category(
        name=category.name,
        description=category.description,
        color=category.color,
        user_id=current_user.id,
    )

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return CategoryResponse(
        id=db_category.id,
        name=db_category.name,
        description=db_category.description,
        color=db_category.color,
        recipe_count=0,
    )


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id, Category.user_id == current_user.id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена"
        )

    recipe_count = db.query(Category.recipes).filter(Category.id == category.id).count()

    return CategoryResponse(
        id=category.id,
        name=category.name,
        description=category.description,
        color=category.color,
        recipe_count=recipe_count,
    )


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_update: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id, Category.user_id == current_user.id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена"
        )

    # Проверка на дубликат имени
    existing = (
        db.query(Category)
        .filter(
            Category.name == category_update.name,
            Category.user_id == current_user.id,
            Category.id != category_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Категория с таким названием уже существует",
        )

    category.name = category_update.name
    category.description = category_update.description
    category.color = category_update.color

    db.commit()
    db.refresh(category)

    recipe_count = db.query(Category.recipes).filter(Category.id == category.id).count()

    return CategoryResponse(
        id=category.id,
        name=category.name,
        description=category.description,
        color=category.color,
        recipe_count=recipe_count,
    )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id, Category.user_id == current_user.id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена"
        )

    # Check if category has associated recipes
    recipe_count = (
        db.query(Recipe)
        .join(Recipe.categories)
        .filter(Category.id == category_id)
        .count()
    )

    if recipe_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Невозможно удалить категорию: она связана с {recipe_count} рецептами. Сначала удалите или перенесите рецепты.",
        )

    db.delete(category)
    db.commit()
