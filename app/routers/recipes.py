import logging
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
    RecipeStatusResponse,
    RecipeUpdate,
)

router = APIRouter(prefix="/recipes", tags=["recipes"])
logger = logging.getLogger(__name__)


def get_user_recipe(recipe_id: int, db: Session, current_user: User) -> Recipe:
    recipe = (
        db.query(Recipe)
        .filter(Recipe.id == recipe_id, Recipe.user_id == current_user.id)
        .first()
    )
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


def validate_category_ids(db: Session, category_ids: list[int]) -> list[Category]:
    if not category_ids:
        return []

    categories = db.query(Category).filter(Category.id.in_(category_ids)).all()

    if len(categories) != len(category_ids):
        missing = set(category_ids) - {cat.id for cat in categories}
        raise HTTPException(status_code=400, detail=f"Categories not found: {missing}")

    return categories


def reset_recipe_review_state(recipe: Recipe) -> None:
    if recipe.publication_status == "approved" and not recipe.is_admin_recipe:
        recipe.visibility = "private"
        recipe.publication_status = "draft"
        recipe.approved_by = None
        recipe.approved_at = None
        recipe.rejection_reason = None


@router.post("/", response_model=RecipeResponse, status_code=201)
def create_recipe(
    recipe: RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category_ids = recipe.category_ids or []
    categories = validate_category_ids(db, category_ids)
    recipe_data = recipe.model_dump(exclude={"category_ids"})

    try:
        db_recipe = Recipe(**recipe_data, user_id=current_user.id)
        db_recipe.categories = categories
        db.add(db_recipe)
        db.commit()
        db.refresh(db_recipe)
        return db_recipe
    except Exception:
        db.rollback()
        logger.exception("Failed to create recipe for user_id=%s", current_user.id)
        raise


@router.get("/", response_model=PaginatedRecipeResponse)
def get_recipes(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Recipe).filter(Recipe.user_id == current_user.id)
    total = query.count()
    recipes = (
        query.order_by(Recipe.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

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

    update_data = updated_recipe.model_dump(exclude_unset=True, exclude={"category_ids"})
    for field, value in update_data.items():
        setattr(recipe, field, value)

    if update_data:
        reset_recipe_review_state(recipe)

    if "category_ids" in updated_recipe.model_dump(exclude_unset=True):
        category_ids = updated_recipe.category_ids
        if category_ids is None or category_ids == []:
            recipe.categories = []
        else:
            categories = validate_category_ids(db, category_ids)
            recipe.categories = categories
        reset_recipe_review_state(recipe)

    db.commit()
    db.refresh(recipe)

    return recipe


@router.post("/{recipe_id}/submit-for-review", response_model=RecipeStatusResponse)
def submit_recipe_for_review(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recipe = get_user_recipe(recipe_id, db, current_user)

    if recipe.is_admin_recipe:
        raise HTTPException(status_code=400, detail="Admin recipes cannot be submitted")

    recipe.visibility = "public"
    recipe.publication_status = "pending_review"
    recipe.rejection_reason = None
    recipe.approved_by = None
    recipe.approved_at = None

    db.commit()
    db.refresh(recipe)

    return RecipeStatusResponse(
        id=recipe.id,
        visibility=recipe.visibility,
        publication_status=recipe.publication_status,
        rejection_reason=recipe.rejection_reason,
        approved_at=recipe.approved_at,
    )


@router.delete("/{recipe_id}", status_code=204)
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recipe = get_user_recipe(recipe_id, db, current_user)

    db.delete(recipe)
    db.commit()
