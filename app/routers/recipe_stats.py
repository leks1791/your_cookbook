from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.category import Category
from app.models.recipe import Recipe
from app.models.user import User

router = APIRouter(prefix="/recipes", tags=["recipes-stats"])


@router.get("/stats")
def get_recipe_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    # Общее количество рецептов
    total_recipes = db.query(Recipe).filter(
        Recipe.user_id == current_user.id
    ).count()

    # Количество категорий
    total_categories = db.query(Category).filter(
        Category.user_id == current_user.id
    ).count()

    # Рецепты за последнюю неделю
    one_week_ago = datetime.now() - timedelta(days=7)
    weekly_recipes = db.query(Recipe).filter(
        Recipe.user_id == current_user.id,
        Recipe.created_at >= one_week_ago
    ).count()

    return {
        "totalRecipes": total_recipes,
        "totalCategories": total_categories,
        "weeklyRecipes": weekly_recipes
    }
