# tests/integration/test_user_routes.py


def test_register_user(client):
    response = client.post(
        "/users/register",
        json={
            "username": "davidtest",
            "email": "davidtest@example.com",
            "password": "SecurePassword123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "davidtest"
    assert data["email"] == "davidtest@example.com"
    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_user(client):
    payload = {
        "username": "duplicate",
        "email": "duplicate@example.com",
        "password": "SecurePassword123",
    }

    first_response = client.post(
        "/users/register",
        json=payload,
    )

    second_response = client.post(
        "/users/register",
        json=payload,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_login_user(client):
    client.post(
        "/users/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "SecurePassword123",
        },
    )

    response = client.post(
        "/users/login",
        json={
            "username": "loginuser",
            "password": "SecurePassword123",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"


def test_login_with_wrong_password(client):
    client.post(
        "/users/register",
        json={
            "username": "wrongpassword",
            "email": "wrongpassword@example.com",
            "password": "SecurePassword123",
        },
    )

    response = client.post(
        "/users/login",
        json={
            "username": "wrongpassword",
            "password": "IncorrectPassword",
        },
    )

    assert response.status_code == 401


def test_registration_rejects_invalid_email(client):
    response = client.post(
        "/users/register",
        json={
            "username": "invalidemail",
            "email": "not-an-email",
            "password": "SecurePassword123",
        },
    )

    assert response.status_code == 422