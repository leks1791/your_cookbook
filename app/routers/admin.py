from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import require_admin
from app.database import get_db
from app.models.category import Category
from app.models.recipe import Recipe
from app.models.user import User
from app.schemas.recipe import (
    AdminRecipeCreate,
    RecipeResponse,
    RecipeStatusResponse,
    ReviewRejectionRequest,
)

router = APIRouter(prefix="/admin", tags=["admin"])


def validate_category_ids(db: Session, category_ids: list[int]) -> list[Category]:
    if not category_ids:
        return []

    categories = db.query(Category).filter(Category.id.in_(category_ids)).all()

    if len(categories) != len(category_ids):
        missing = set(category_ids) - {cat.id for cat in categories}
        raise HTTPException(status_code=400, detail=f"Categories not found: {missing}")

    return categories


def get_recipe_for_moderation(recipe_id: int, db: Session) -> Recipe:
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.get("/recipes/pending", response_model=list[RecipeResponse])
def get_pending_recipes(
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    return (
        db.query(Recipe)
        .filter(Recipe.publication_status == "pending_review")
        .order_by(Recipe.created_at.desc())
        .all()
    )


@router.post("/recipes", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
def create_admin_recipe(
    recipe: AdminRecipeCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    categories = validate_category_ids(db, recipe.category_ids or [])
    recipe_data = recipe.model_dump(exclude={"category_ids", "visibility"})

    db_recipe = Recipe(
        **recipe_data,
        user_id=current_admin.id,
        visibility="public",
        publication_status="approved",
        is_admin_recipe=True,
        approved_by=current_admin.id,
        approved_at=datetime.now(UTC),
    )
    db_recipe.categories = categories

    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


@router.post("/recipes/{recipe_id}/approve", response_model=RecipeStatusResponse)
def approve_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    recipe = get_recipe_for_moderation(recipe_id, db)
    recipe.visibility = "public"
    recipe.publication_status = "approved"
    recipe.approved_by = current_admin.id
    recipe.approved_at = datetime.now(UTC)
    recipe.rejection_reason = None

    db.commit()
    db.refresh(recipe)

    return RecipeStatusResponse(
        id=recipe.id,
        visibility=recipe.visibility,
        publication_status=recipe.publication_status,
        rejection_reason=recipe.rejection_reason,
        approved_at=recipe.approved_at,
    )


@router.post("/recipes/{recipe_id}/reject", response_model=RecipeStatusResponse)
def reject_recipe(
    recipe_id: int,
    payload: ReviewRejectionRequest,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin),
):
    recipe = get_recipe_for_moderation(recipe_id, db)
    recipe.visibility = "private"
    recipe.publication_status = "rejected"
    recipe.rejection_reason = payload.reason
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
