import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.category import Category
from app.models.recipe import Recipe
from app.models.user import User
from app.schemas.recipe import (
    PaginatedRecipeResponse,
    RecipeCreate,
    RecipeResponse,
    RecipeUpdate,
)

router = APIRouter(prefix="/recipes", tags=["recipes"])


def get_user_recipe(recipe_id: int, db: Session, current_user: User) -> Recipe:
    """Получить рецепт, принадлежащий текущему пользователю."""
    recipe = (
        db.query(Recipe)
        .filter(Recipe.id == recipe_id, Recipe.user_id == current_user.id)
        .first()
    )
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


def validate_category_ids(db: Session, category_ids: list[int]) -> list[Category]:
    """Валидация и получение категорий по ID."""
    if not category_ids:
        return []

    categories = db.query(Category).filter(Category.id.in_(category_ids)).all()

    if len(categories) != len(category_ids):
        missing = set(category_ids) - {cat.id for cat in categories}
        raise HTTPException(status_code=400, detail=f"Categories not found: {missing}")

    return categories


@router.post("/", response_model=RecipeResponse, status_code=201)
def create_recipe(
    recipe: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Валидация категорий
    category_ids = recipe.category_ids or []
    categories = validate_category_ids(db, category_ids)

    # Создаём рецепт без categories (они будут добавлены отдельно)
    recipe_data = recipe.model_dump(exclude={"category_ids"})
    db_recipe = Recipe(**recipe_data, user_id=current_user.id)
    db_recipe.categories = categories

    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


@router.get("/", response_model=PaginatedRecipeResponse)
def get_recipes(
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(10, ge=1, le=100, description="Количество на странице"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Recipe).filter(Recipe.user_id == current_user.id)
    total = query.count()
    recipes = query.offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedRecipeResponse(
        items=recipes,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size) if total > 0 else 1,
    )


@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_recipe(recipe_id, db, current_user)


@router.put("/{recipe_id}", response_model=RecipeResponse)
def update_recipe(
    recipe_id: int,
    updated_recipe: RecipeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recipe = get_user_recipe(recipe_id, db, current_user)

    # Обновляем базовые поля (исключая category_ids)
    update_data = updated_recipe.model_dump(
        exclude_unset=True, exclude={"category_ids"}
    )
    for field, value in update_data.items():
        setattr(recipe, field, value)

    # Обновляем категории если переданы
    if "category_ids" in updated_recipe.model_dump(exclude_unset=True):
        category_ids = updated_recipe.category_ids
        # Если category_ids None или пустой список - очищаем категории
        if category_ids is None or category_ids == []:
            recipe.categories = []
        else:
            # Валидируем и устанавливаем новые категории
            categories = validate_category_ids(db, category_ids)
            recipe.categories = categories

    db.commit()
    db.refresh(recipe)

    return recipe


@router.delete("/{recipe_id}", status_code=204)
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recipe = get_user_recipe(recipe_id, db, current_user)

    db.delete(recipe)
    db.commit()
