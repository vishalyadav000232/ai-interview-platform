import pytest


@pytest.mark.asyncio
async def test_refresh_token_success(client):
    register_response = await client.post(
        "/auth/register",
        json={
            "first_name": "vishal",
            "last_name": "yadav",
            "email": "refreshsuccess@example.com",
            "password": "vishal123"
        }
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/auth/login",
        data={
            "username": "refreshsuccess@example.com",
            "password": "vishal123"
        }
    )

    assert login_response.status_code == 200

    response = await client.post("/auth/refresh")

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["data"]["access_token"] is not None
    assert data["data"]["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_refresh_token_missing(client):
    client.cookies.clear()

    response = await client.post("/auth/refresh")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token_invalid(client):
    client.cookies.clear()

    client.cookies.set(
        "refresh_token", "invalid-refresh-token"
    )

    response = await client.post("/auth/refresh")

    assert response.status_code == 401


