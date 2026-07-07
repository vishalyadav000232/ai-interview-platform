import pytest
from uuid import uuid4


def unique_email():
    return f"test_{uuid4().hex}@example.com"


async def register_user(client, email: str, password: str = "vishal123"):
    response = await client.post(
        "/auth/register",
        json={
            "first_name": "Vishal",
            "last_name": "Yadav",
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 201
    return response.json()


async def login_user(client, email: str, password: str = "vishal123"):
    response = await client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert response.status_code == 200
    return response.json()


@pytest.mark.asyncio
async def test_get_current_user_success(client):
    email = unique_email()
    password = "vishal123"

    await register_user(client, email, password)

    login_data = await login_user(client, email, password)

    access_token = login_data["access_token"]
    print(access_token)

    response = await client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    

    user_data = data

    assert user_data["email"] == email
    assert user_data["first_name"] == "Vishal"
    assert user_data["id"] is not None


@pytest.mark.asyncio
async def test_get_current_user_missing_token(client):
    response = await client.get("/auth/me")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(client):
    response = await client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer invalid.token.here"
        },
    )

    assert response.status_code == 401