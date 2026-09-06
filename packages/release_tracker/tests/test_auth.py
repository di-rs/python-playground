from collections.abc import Callable

from fastapi.testclient import TestClient
from release_tracker.models import User


def test_login_returns_token(
    client: TestClient, make_user: Callable[..., User]
) -> None:
    make_user(email="login@example.com", password="correct-password")

    response = client.post(
        "/auth/token",
        data={
            "username": "login@example.com",
            "password": "correct-password",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert isinstance(body["access_token"], str)
    assert len(body["access_token"]) > 0


def test_login_wrong_password_returns_401(
    client: TestClient, make_user: Callable[..., User]
) -> None:
    make_user(email="login@example.com", password="correct-password")

    response = client.post(
        "/auth/token",
        data={
            "username": "login@example.com",
            "password": "WRONG",
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or password"}


def test_login_unknown_user_returns_401(client: TestClient) -> None:
    response = client.post(
        "/auth/token",
        data={
            "username": "nobody@example.com",
            "password": "anything",
        },
    )
    assert response.status_code == 401


def test_inactive_user_cannot_log_in(
    client: TestClient, make_user: Callable[..., User]
) -> None:
    make_user(email="frozen@example.com", password="pw", is_active=False)

    response = client.post(
        "/auth/token",
        data={
            "username": "frozen@example.com",
            "password": "pw",
        },
    )
    assert response.status_code == 401


def test_me_endpoint_returns_current_user(auth_client: TestClient) -> None:
    response = auth_client.get("/auth/me")
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "editor@example.com"
    assert body["is_active"] is True
    assert "hashed_password" not in body


def test_me_endpoint_rejects_missing_token(client: TestClient) -> None:
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_me_endpoint_rejects_garbage_token(client: TestClient) -> None:
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer not-a-real-jwt"},
    )
    assert response.status_code == 401


def test_register_creates_user(client: TestClient) -> None:
    response = client.post(
        "/auth/register",
        json={"email": "test@test.com", "password": "test-password"},
    )
    assert response.status_code == 201

    data = response.json()
    assert data["email"] == "test@test.com"
    assert data["is_active"]
    assert "hashed_password" not in data


def test_register_then_login(client: TestClient) -> None:
    client.post(
        "/auth/register",
        json={"email": "test@test.com", "password": "test-password"},
    )
    response = client.post(
        "/auth/token",
        data={
            "username": "test@test.com",
            "password": "test-password",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data["access_token"], str)
    assert len(data["access_token"]) > 0
