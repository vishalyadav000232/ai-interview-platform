# tests/test_email_verification.py

import pytest


@pytest.mark.asyncio
async def test_verify_email_success(client):
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": "verify_success@example.com",
        "password": "password123"
    }

    register_response = await client.post(
        "/auth/register",
        json=payload
    )

    assert register_response.status_code == 201

    data = register_response.json()
    verification_link = data["data"]["verification_link"]

    verify_url = verification_link.replace(
        "http://localhost:8001",
        ""
    )

    verify_response = await client.get(verify_url)

    assert verify_response.status_code == 200

    verify_data = verify_response.json()

    assert verify_data["success"] is True
    assert verify_data["message"] == "Email verified successfully"
    
@pytest.mark.asyncio
async def test_verify_email_invalid_token(client):

    response = await client.get(
        "/auth/verify-email?token=invalid-token"
    )

    assert response.status_code == 401

import pytest


@pytest.mark.asyncio
async def test_verify_email_already_verified(client):
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": "already_verified@example.com",
        "password": "password123"
    }

    register_response = await client.post(
        "/auth/register",
        json=payload
    )

    assert register_response.status_code == 201

    verification_link = register_response.json()["data"]["verification_link"]

    verify_url = verification_link.replace(
        "http://localhost:8001",
        ""
    )

    first_response = await client.get(verify_url)
    assert first_response.status_code == 200

    second_response = await client.get(verify_url)
    assert second_response.status_code == 200

    data = second_response.json()

    assert data["success"] is True



@pytest.mark.asyncio
async def test_resend_verification_success(client):
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": "resend_success@example.com",
        "password": "password123"
    }

    register_response = await client.post(
        "/auth/register",
        json=payload
    )

    assert register_response.status_code == 201
    
    
    login_response = await client.post("/auth/login" , 
                                       data={
            "username": payload["email"],
            "password": payload["password"]
        })
    
    access_token  =  login_response.json()["access_token"] 


    response = await client.post(
        "/auth/resend-verification",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Verification email sent successfully"
    assert data["data"]["verification_link"] is not None
    
    

@pytest.mark.asyncio
async def test_resend_verification_already_verified(client):
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": "resend_already_verified@example.com",
        "password": "password123"
    }

    register_response = await client.post(
        "/auth/register",
        json=payload
    )

    assert register_response.status_code == 201

    data = register_response.json()["data"]

    login_response = await client.post("/auth/login" , 
                                       data={
            "username": payload["email"],
            "password": payload["password"]
        })
    
    access_token  =  login_response.json()["access_token"] 

    verification_link = data["verification_link"]

    verify_url = verification_link.replace(
        "http://localhost:8001",
        ""
    )

    verify_response = await client.get(verify_url)
    assert verify_response.status_code == 200

    response = await client.post(
        "/auth/resend-verification",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 400