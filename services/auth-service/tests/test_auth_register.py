import pytest
from uuid import uuid4


def unique_email():
    return f"test_{uuid4().hex}@example.com"


@pytest.mark.asyncio
async def test_register_user_success(client):
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": unique_email(),
        "password": "vishal123"
    }

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["success"] is True

    user_data = data["data"]["user"]

    assert user_data["id"] is not None
    assert user_data["email"] == payload["email"]
    assert user_data["first_name"] == payload["first_name"]


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": unique_email(),
        "password": "vishal123"
    }

    first_response = await client.post("/auth/register", json=payload)
    assert first_response.status_code == 201

    second_response = await client.post("/auth/register", json=payload)

    assert second_response.status_code == 409

    data = second_response.json()

    assert data["success"] is False


@pytest.mark.asyncio
async def test_register_invalid_email(client):
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": "invalid-email",
        "password": "vishal123"
    }

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_missing_password(client):
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": unique_email()
    }

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_missing_email(client):
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "password": "vishal123"
    }

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_missing_first_name(client):
    payload = {
        "last_name": "Yadav",
        "email": unique_email(),
        "password": "vishal123"
    }

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_empty_first_name(client):
    payload = {
        "first_name": "",
        "last_name": "Yadav",
        "email": unique_email(),
        "password": "vishal123"
    }

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_empty_email(client):
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": "",
        "password": "vishal123"
    }

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_empty_password(client):
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": unique_email(),
        "password": ""
    }

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_short_password(client):
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": unique_email(),
        "password": "123"
    }

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 422