import math

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.recipe import Recipe
from app.models.user import User
from app.schemas.recipe import PaginatedRecipeResponse, RecipeResponse

router = APIRouter(prefix="/catalog", tags=["catalog"])


def get_public_recipe(recipe_id: int, db: Session) -> Recipe:
    recipe = (
        db.query(Recipe)
        .filter(
            Recipe.id == recipe_id,
            Recipe.visibility == "public",
            Recipe.publication_status == "approved",
        )
        .first()
    )
    if not recipe:
        raise HTTPException(status_code=404, detail="Catalog recipe not found")
    return recipe


@router.get("", response_model=PaginatedRecipeResponse)
def get_catalog(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    source: str | None = Query(None, pattern="^(admin|community)$"),
    db: Session = Depends(get_db),
):
    query = db.query(Recipe).filter(
        Recipe.visibility == "public",
        Recipe.publication_status == "approved",
    )

    if source == "admin":
        query = query.filter(Recipe.is_admin_recipe.is_(True))
    elif source == "community":
        query = query.filter(Recipe.is_admin_recipe.is_(False))

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
def get_catalog_recipe(recipe_id: int, db: Session = Depends(get_db)):
    return get_public_recipe(recipe_id, db)


@router.post(
    "/{recipe_id}/clone",
    response_model=RecipeResponse,
    status_code=status.HTTP_201_CREATED,
)
def clone_catalog_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    source_recipe = get_public_recipe(recipe_id, db)

    cloned_recipe = Recipe(
        title=source_recipe.title,
        description=source_recipe.description,
        ingredients=source_recipe.ingredients,
        steps=source_recipe.steps,
        tags=source_recipe.tags,
        photos=source_recipe.photos,
        prep_time=source_recipe.prep_time,
        cook_time=source_recipe.cook_time,
        servings=source_recipe.servings,
        difficulty=source_recipe.difficulty,
        cuisine=source_recipe.cuisine,
        notes=source_recipe.notes,
        visibility="private",
        publication_status="draft",
        is_admin_recipe=False,
        original_recipe_id=source_recipe.id,
        user_id=current_user.id,
    )
    cloned_recipe.categories = list(source_recipe.categories)

    db.add(cloned_recipe)
    db.commit()
    db.refresh(cloned_recipe)
    return cloned_recipe
