import pytest


@pytest.mark.asyncio
async def test_register_user_success(client):
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": "vishaltest228379413clear@example.com",
        "password": "vishal123"
    }

    response = await client.post(
        "/auth/register",
        json=payload
    )

    assert response.status_code == 201

    data = response.json()

    assert data["success"] is True

    user_data = data["data"]["user"]

    assert user_data["email"] == payload["email"]
    assert user_data["first_name"] == payload["first_name"]
    assert user_data["id"] is not None


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": "duplicateew1@example.com",
        "password": "vishal123"
    }

    first_response = await client.post(
        "/auth/register",
        json=payload
    )

    assert first_response.status_code == 201

    
    second_response = await client.post(
        "/auth/register",
        json=payload
    )

    assert second_response.status_code in [400, 409]

    data = second_response.json()

    assert data["success"] is False