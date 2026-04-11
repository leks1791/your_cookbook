import pytest


def test_create_recipe(client, auth_headers):
    response = client.post(
        "/recipes/",
        json={
            "title": "Test Recipe",
            "description": "Test description",
            "ingredients": "ingredient1, ingredient2",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Recipe"
    assert data["description"] == "Test description"
    assert data["ingredients"] == "ingredient1, ingredient2"


def test_get_recipes(client, auth_headers, db, test_user):
    # Создаём рецепты
    from app.models.recipe import Recipe
    
    recipe1 = Recipe(
        title="Recipe 1",
        description="Desc 1",
        ingredients="ing1",
        user_id=test_user.id,
    )
    recipe2 = Recipe(
        title="Recipe 2",
        description="Desc 2",
        ingredients="ing2",
        user_id=test_user.id,
    )
    db.add_all([recipe1, recipe2])
    db.commit()

    response = client.get("/recipes/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_get_recipes_pagination(client, auth_headers, db, test_user):
    from app.models.recipe import Recipe
    
    for i in range(15):
        recipe = Recipe(
            title=f"Recipe {i}",
            description=f"Desc {i}",
            ingredients=f"ing{i}",
            user_id=test_user.id,
        )
        db.add(recipe)
    db.commit()

    response = client.get("/recipes/?page=1&page_size=10", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 15
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert data["total_pages"] == 2
    assert len(data["items"]) == 10


def test_get_recipe_by_id(client, auth_headers, db, test_user):
    from app.models.recipe import Recipe
    
    recipe = Recipe(
        title="Test Recipe",
        description="Desc",
        ingredients="ing",
        user_id=test_user.id,
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    response = client.get(f"/recipes/{recipe.id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Recipe"


def test_update_recipe(client, auth_headers, db, test_user):
    from app.models.recipe import Recipe
    
    recipe = Recipe(
        title="Original Title",
        description="Original Desc",
        ingredients="original ing",
        user_id=test_user.id,
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    response = client.put(
        f"/recipes/{recipe.id}",
        json={
            "title": "Updated Title",
            "description": "Updated Desc",
            "ingredients": "updated ing",
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"


def test_delete_recipe(client, auth_headers, db, test_user):
    from app.models.recipe import Recipe
    
    recipe = Recipe(
        title="To Delete",
        description="Desc",
        ingredients="ing",
        user_id=test_user.id,
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    recipe_id = recipe.id

    response = client.delete(f"/recipes/{recipe_id}", headers=auth_headers)
    assert response.status_code == 204

    # Проверяем, что удалено
    response = client.get(f"/recipes/{recipe_id}", headers=auth_headers)
    assert response.status_code == 404


def test_cannot_access_other_user_recipe(client, auth_headers, db):
    from app.models.recipe import Recipe
    
    # Рецепт другого пользователя (без user_id - не принадлежит текущему)
    other_user = User(
        username="otheruser",
        email="other@example.com",
        hashed_password="hash",
    )
    db.add(other_user)
    db.commit()
    db.refresh(other_user)

    recipe = Recipe(
        title="Other User Recipe",
        description="Desc",
        ingredients="ing",
        user_id=other_user.id,
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    response = client.get(f"/recipes/{recipe.id}", headers=auth_headers)
    assert response.status_code == 404


# Импорт для теста
from app.models.user import User
