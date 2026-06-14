import pytest
from uuid import uuid4


def unique_email():
    return f"test_{uuid4().hex}@example.com"


@pytest.mark.asyncio
async def test_login_success(client):

    email = unique_email()

    register_payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": email,
        "password": "vishal123"
    }

    register_response = await client.post(
        "/auth/register",
        json=register_payload
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "vishal123"
        }
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert data["success"] is True

    assert "access_token" in data
    
    
@pytest.mark.asyncio
async def test_login_wrong_password(client):

    email = unique_email()

    await client.post(
        "/auth/register",
        json={
            "first_name": "Vishal",
            "last_name": "Yadav",
            "email": email,
            "password": "vishal123"
        }
    )

    response = await client.post(
        "/auth/login",
        data={
            "username": email,
            "password": "wrongpassword"
        }
    )

    assert response.status_code in [400, 401]

    data = response.json()

    assert data["success"] is False
    
@pytest.mark.asyncio
async def test_login_user_not_found(client):

    response = await client.post(
        "/auth/login",
        data={
            "username": "nouser@example.com",
            "password": "vishal123"
        }
    )

    assert response.status_code in [400, 401]

    data = response.json()

    assert data["success"] is False

@pytest.mark.asyncio
async def test_login_missing_password(client):

    response = await client.post(
        "/auth/login",
        data={
            "username": "test@example.com"
        }
    )

    assert response.status_code == 422

@pytest.mark.asyncio
async def test_login_missing_username(client):

    response = await client.post(
        "/auth/login",
        data={
            "password": "vishal123"
        }
    )

    assert response.status_code == 422