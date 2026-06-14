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
    

@pytest.mark.asyncio
async def test_refresh_token_rotation(client):
    await client.post(
        "/auth/register",
        json={
            "first_name": "vishal",
            "last_name": "yadav",
            "email": "rotation@example.com",
            "password": "vishal123"
        }
    )

    login_response = await client.post(
        "/auth/login",
        data={
            "username": "rotation@example.com",
            "password": "vishal123"
        }
    )

    assert login_response.status_code == 200

    old_refresh_token = client.cookies.get("refresh_token")
    assert old_refresh_token is not None

    refresh_response = await client.post("/auth/refresh")
    assert refresh_response.status_code == 200

    new_refresh_token = client.cookies.get("refresh_token")
    assert new_refresh_token is not None
    assert new_refresh_token != old_refresh_token

    client.cookies.set(
        "refresh_token",
        old_refresh_token
    )

    reuse_response = await client.post("/auth/refresh")

    assert reuse_response.status_code == 401

@pytest.mark.asyncio
async def test_logout_without_refresh_token(client):
    client.cookies.clear()

    response = await client.post("/auth/logout")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout_invalid_refresh_token(client):
    client.cookies.clear()

    client.cookies.set(
        "refresh_token",
        "invalid-refresh-token"
    )

    response = await client.post("/auth/logout")

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_logout_without_refresh_token(client):
    client.cookies.clear()

    response = await client.post("/auth/logout")

    assert response.status_code == 401



