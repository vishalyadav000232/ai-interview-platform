import pytest


@pytest.mark.asyncio
async def test_logout_success(client):

    await client.post(
        "/auth/register",
        json={
            "first_name": "vishal",
            "email": "logout@example.com",
            "password": "vishal123"
        }
    )

    login_response = await client.post(
        "/auth/login",
        data={
            "username": "logout@example.com",
            "password": "vishal123"
        }
    )

    assert login_response.status_code == 200

    response = await client.post(
        "/auth/logout"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    
    

@pytest.mark.asyncio
async def test_refresh_after_logout(client):
    await client.post(
        "/auth/register",
        json={
            "first_name": "vishal",
            "last_name": "yadav",
            "email": "refreshlogout@example.com",
            "password": "vishal123"
        }
    )

    login_response = await client.post(
        "/auth/login",
        data={
            "username": "refreshlogout@example.com",
            "password": "vishal123"
        }
    )

    assert login_response.status_code == 200

    logout_response = await client.post("/auth/logout")

    assert logout_response.status_code == 200

    response = await client.post("/auth/refresh")

    assert response.status_code == 401