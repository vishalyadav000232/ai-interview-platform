# tests/test_reset_password.py

import pytest


@pytest.mark.asyncio
async def test_forgot_password_success(client):
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": "yv096203@gmail.com",
        "password": "oldpassword123"
    }

    register_response = await client.post("/auth/register", json=payload)
    assert register_response.status_code == 201

    response = await client.post(
        "/auth/forgot-password",
        json={"email": payload["email"]}
    )

    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert data["message"] == (
        "If this email exists, password reset instructions have been sent"
    )


@pytest.mark.asyncio
async def test_forgot_password_unknown_email_returns_same_response(client):
    response = await client.post(
        "/auth/forgot-password",
        json={"email": "unknown_user@example.com"}
    )

    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert data["message"] == (
        "If this email exists, password reset instructions have been sent"
    )


@pytest.mark.asyncio
async def test_reset_password_success(client):
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": "reset_success@example.com",
        "password": "oldpassword123"
    }

    register_response = await client.post("/auth/register", json=payload)
    assert register_response.status_code == 201

    data = register_response.json()["data"]

    # Testing shortcut:
    # Register response me access_token mil raha hai, but reset token nahi.
    # Isliye hum forgot-password route ko direct token return karne ke liye
    # testing mode me use kar sakte hain agar tum return kar rahe ho.
    forgot_response = await client.post(
        "/auth/forgot-password",
        json={"email": payload["email"]}
    )

    assert forgot_response.status_code == 200

    forgot_data = forgot_response.json()

    reset_link = forgot_data.get("data", {}).get("reset_link")

    assert reset_link is not None

    reset_token = reset_link.split("token=")[1]

    reset_response = await client.post(
        "/auth/reset-password",
        json={
            "token": reset_token,
            "new_password": "newpassword123"
        }
    )

    assert reset_response.status_code == 200

    reset_data = reset_response.json()
    assert reset_data["success"] is True
    assert reset_data["message"] == "Password reset successfully"

    old_login_response = await client.post(
        "/auth/login",
        data={
            "username": payload["email"],
            "password": "oldpassword123"
        }
    )

    assert old_login_response.status_code == 401

    new_login_response = await client.post(
        "/auth/login",
        data={
            "username": payload["email"],
            "password": "newpassword123"
        }
    )

    assert new_login_response.status_code == 200


@pytest.mark.asyncio
async def test_reset_password_invalid_token(client):
    response = await client.post(
        "/auth/reset-password",
        json={
            "token": "invalid-token",
            "new_password": "newpassword123"
        }
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_reset_password_short_password(client):
    response = await client.post(
        "/auth/reset-password",
        json={
            "token": "fake-token",
            "new_password": "123"
        }
    )

    assert response.status_code == 422