from app.models.recipe import Recipe


def test_submit_recipe_for_review(client, auth_headers, db, test_user):
    recipe = Recipe(
        title="My Recipe",
        description="Desc",
        ingredients="ing",
        user_id=test_user.id,
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    response = client.post(f"/recipes/{recipe.id}/submit-for-review", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["visibility"] == "public"
    assert data["publication_status"] == "pending_review"


def test_non_admin_cannot_access_admin_pending(client, auth_headers):
    response = client.get("/admin/recipes/pending", headers=auth_headers)
    assert response.status_code == 403


def test_admin_can_approve_recipe(client, admin_auth_headers, db, test_user):
    recipe = Recipe(
        title="Public Candidate",
        description="Desc",
        ingredients="ing",
        visibility="public",
        publication_status="pending_review",
        user_id=test_user.id,
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    response = client.post(f"/admin/recipes/{recipe.id}/approve", headers=admin_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["publication_status"] == "approved"
    assert data["visibility"] == "public"


def test_admin_can_reject_recipe(client, admin_auth_headers, db, test_user):
    recipe = Recipe(
        title="Reject Candidate",
        description="Desc",
        ingredients="ing",
        visibility="public",
        publication_status="pending_review",
        user_id=test_user.id,
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    response = client.post(
        f"/admin/recipes/{recipe.id}/reject",
        json={"reason": "Needs better instructions"},
        headers=admin_auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["publication_status"] == "rejected"
    assert data["visibility"] == "private"
    assert data["rejection_reason"] == "Needs better instructions"


def test_catalog_shows_only_approved_recipes(client, db, admin_user, test_user):
    approved_recipe = Recipe(
        title="Approved",
        description="Desc",
        ingredients="ing",
        visibility="public",
        publication_status="approved",
        user_id=admin_user.id,
        is_admin_recipe=True,
    )
    pending_recipe = Recipe(
        title="Pending",
        description="Desc",
        ingredients="ing",
        visibility="public",
        publication_status="pending_review",
        user_id=test_user.id,
    )
    db.add_all([approved_recipe, pending_recipe])
    db.commit()

    response = client.get("/catalog")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Approved"


def test_clone_catalog_recipe_creates_private_copy(
    client, auth_headers, db, admin_user, test_user
):
    source_recipe = Recipe(
        title="Admin Recipe",
        description="Desc",
        ingredients="ing",
        visibility="public",
        publication_status="approved",
        is_admin_recipe=True,
        user_id=admin_user.id,
    )
    db.add(source_recipe)
    db.commit()
    db.refresh(source_recipe)

    response = client.post(f"/catalog/{source_recipe.id}/clone", headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Admin Recipe"
    assert data["visibility"] == "private"
    assert data["publication_status"] == "draft"
    assert data["original_recipe_id"] == source_recipe.id
    assert data["user_id"] == test_user.id


def test_updating_approved_user_recipe_resets_review_state(client, auth_headers, db, test_user):
    recipe = Recipe(
        title="Approved User Recipe",
        description="Desc",
        ingredients="ing",
        visibility="public",
        publication_status="approved",
        user_id=test_user.id,
    )
    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    response = client.put(
        f"/recipes/{recipe.id}",
        json={"title": "Updated Recipe"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Recipe"
    assert data["visibility"] == "private"
    assert data["publication_status"] == "draft"
