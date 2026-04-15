def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert data["role"] == "user"
    assert "id" in data


def test_register_duplicate_email(client, test_user):
    response = client.post(
        "/auth/register",
        json={
            "username": "otheruser",
            "email": "test@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 400


def test_register_duplicate_username(client, test_user):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "other@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 400


def test_register_short_password(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "user",
            "email": "user@example.com",
            "password": "123",
        },
    )
    assert response.status_code == 422


def test_login_success(client, test_user):
    response = client.post(
        "/auth/login",
        json={"email_or_username": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_by_email_field(client, test_user):
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_by_username(client, test_user):
    response = client.post(
        "/auth/login",
        json={"email_or_username": "testuser", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client, test_user):
    response = client.post(
        "/auth/login",
        json={"email_or_username": "test@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post(
        "/auth/login",
        json={
            "email_or_username": "nonexistent@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 401


def test_me_returns_role(client, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["role"] == "user"
