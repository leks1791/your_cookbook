from datetime import datetime, timedelta
import json

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.recipe import Recipe
from app.models.user import User

router = APIRouter(prefix="/recipes", tags=["recipes-stats"])


@router.get("/stats")
def get_recipe_stats(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> dict:
    # Общее количество рецептов
    total_recipes = db.query(Recipe).filter(Recipe.user_id == current_user.id).count()

    # Количество уникальных тегов
    recipes = db.query(Recipe).filter(Recipe.user_id == current_user.id).all()
    unique_tags = set()
    for recipe in recipes:
        try:
            tags = json.loads(recipe.tags) if recipe.tags else []
            if isinstance(tags, str):
                tags = json.loads(tags)
            unique_tags.update(tags)
        except (json.JSONDecodeError, TypeError):
            continue

    # Рецепты за последнюю неделю
    one_week_ago = datetime.now() - timedelta(days=7)
    weekly_recipes = (
        db.query(Recipe)
        .filter(Recipe.user_id == current_user.id, Recipe.created_at >= one_week_ago)
        .count()
    )

    return {
        "totalRecipes": total_recipes,
        "totalTags": len(unique_tags),
        "weeklyRecipes": weekly_recipes,
    }


@router.get("/tags")
def get_tags_with_counts(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[dict]:
    """Получить все уникальные теги с количеством рецептов для текущего пользователя"""
    recipes = db.query(Recipe).filter(Recipe.user_id == current_user.id).all()

    tag_counts: dict[str, int] = {}

    for recipe in recipes:
        try:
            tags = json.loads(recipe.tags) if recipe.tags else []
            if isinstance(tags, str):
                tags = json.loads(tags)
            for tag in tags:
                if tag:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
        except (json.JSONDecodeError, TypeError):
            continue

    # Сортируем по количеству (по убыванию) и затем по названию
    result = [
        {"name": tag, "count": count}
        for tag, count in sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))
    ]

    return result


@router.get("/tag/{tag_name}")
def get_recipes_by_tag(
    tag_name: str,
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(10, ge=1, le=100, description="Количество на странице"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Получить рецепты по тегу"""
    # Получаем все рецепты пользователя
    recipes = db.query(Recipe).filter(Recipe.user_id == current_user.id).all()

    # Фильтруем по тегу
    filtered_recipes = []
    for recipe in recipes:
        try:
            tags = json.loads(recipe.tags) if recipe.tags else []
            if isinstance(tags, str):
                tags = json.loads(tags)
            if tag_name in tags:
                filtered_recipes.append(recipe)
        except (json.JSONDecodeError, TypeError):
            continue

    # Пагинация
    total = len(filtered_recipes)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_recipes = filtered_recipes[start:end]

    total_pages = (total + page_size - 1) // page_size if total > 0 else 1

    # Конвертируем модели в словари для сериализации
    def recipe_to_dict(recipe):
        return {
            "id": recipe.id,
            "title": recipe.title,
            "description": recipe.description,
            "ingredients": recipe.ingredients,
            "steps": recipe.steps,
            "tags": json.loads(recipe.tags) if recipe.tags else [],
            "photos": json.loads(recipe.photos) if recipe.photos else [],
            "prep_time": recipe.prep_time,
            "cook_time": recipe.cook_time,
            "servings": recipe.servings,
            "difficulty": recipe.difficulty,
            "cuisine": recipe.cuisine,
            "notes": recipe.notes,
            "user_id": recipe.user_id,
            "created_at": recipe.created_at.isoformat() if recipe.created_at else None,
            "updated_at": recipe.updated_at.isoformat() if recipe.updated_at else None,
            "categories": [
                {"id": cat.id, "name": cat.name, "color": cat.color}
                for cat in recipe.categories
            ],
        }

    return {
        "items": [recipe_to_dict(r) for r in paginated_recipes],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "tag": tag_name,
    }
