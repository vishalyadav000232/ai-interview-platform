import pytest


@pytest.mark.asyncio
async def test_change_password_success(client):
    # register
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": "changepass_success@example.com",
        "password": "oldpassword123"
    }

    register_response = await client.post("/auth/register", json=payload)
    assert register_response.status_code == 201
    
    
    
    login_response = await client.post("/auth/login" , 
                                       data={
            "username": payload["email"],
            "password": payload["password"]
        })
    
    access_token  =  login_response.json()["access_token"]     

    response = await client.post(
        "/auth/change-password",
        json={
            "old_password": "oldpassword123",
            "new_password": "newpassword123"
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Password changed successfully"


@pytest.mark.asyncio
async def test_change_password_wrong_old_password(client):
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": "changepass_wrong@example.com",
        "password": "oldpassword123"
    }

    register_response = await client.post("/auth/register", json=payload)
    assert register_response.status_code == 201

    login_response = await client.post("/auth/login" , 
                                       data={
            "username": payload["email"],
            "password": payload["password"]
        })
    
    access_token  =  login_response.json()["access_token"] 

    response = await client.post(
        "/auth/change-password",
        json={
            "old_password": "wrongpassword",
            "new_password": "newpassword123"
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_change_password_without_token(client):
    response = await client.post(
        "/auth/change-password",
        json={
            "old_password": "oldpassword123",
            "new_password": "newpassword123"
        }
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_change_password_short_new_password(client):
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": "changepass_short@example.com",
        "password": "oldpassword123"
    }

    register_response = await client.post("/auth/register", json=payload)
    assert register_response.status_code == 201

    login_response = await client.post("/auth/login" , 
                                       data={
            "username": payload["email"],
            "password": payload["password"]
        })
    
    access_token  =  login_response.json()["access_token"] 


    response = await client.post(
        "/auth/change-password",
        json={
            "old_password": "oldpassword123",
            "new_password": "123"
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_change_password_login_with_old_password_fails(client):
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": "changepass_old_login@example.com",
        "password": "oldpassword123"
    }

    register_response = await client.post("/auth/register", json=payload)
    assert register_response.status_code == 201

    login_response = await client.post("/auth/login" , 
                                       data={
            "username": payload["email"],
            "password": payload["password"]
        })
    
    access_token  =  login_response.json()["access_token"] 


    change_response = await client.post(
        "/auth/change-password",
        json={
            "old_password": "oldpassword123",
            "new_password": "newpassword123"
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert change_response.status_code == 200

    login_response = await client.post(
        "/auth/login",
        data={
            "username": payload["email"],
            "password": "oldpassword123"
        }
    )

    assert login_response.status_code == 401


@pytest.mark.asyncio
async def test_change_password_login_with_new_password_success(client):
    payload = {
        "first_name": "Vishal",
        "last_name": "Yadav",
        "email": "changepass_new_login@example.com",
        "password": "oldpassword123"
    }

    register_response = await client.post("/auth/register", json=payload)
    assert register_response.status_code == 201

    login_response = await client.post("/auth/login" , 
                                       data={
            "username": payload["email"],
            "password": payload["password"]
        })
    
    access_token  =  login_response.json()["access_token"] 

    change_response = await client.post(
        "/auth/change-password",
        json={
            "old_password": "oldpassword123",
            "new_password": "newpassword123"
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert change_response.status_code == 200

    login_response = await client.post(
        "/auth/login",
        data={
            "username": payload["email"],
            "password": "newpassword123"
        }
    )

    assert login_response.status_code == 200