def test_signup(client):
    response = client.post(
        "/auth/signup",
        json={
            "email": "test@example.com",
            "password": "password123",
            "full_name": "Test User"
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "token" in data
    assert data["user"]["email"] == "test@example.com"

def test_signup_duplicate_email(client):
    # First signup
    client.post(
        "/auth/signup",
        json={
            "email": "duplicate@example.com",
            "password": "password123",
            "full_name": "Test User"
        },
    )
    # Second signup
    response = client.post(
        "/auth/signup",
        json={
            "email": "duplicate@example.com",
            "password": "password123",
            "full_name": "Test User"
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login(client):
    # Setup user
    client.post(
        "/auth/signup",
        json={
            "email": "login@example.com",
            "password": "password123",
            "full_name": "Login User"
        },
    )
    
    # Login
    response = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "password123"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["user"]["email"] == "login@example.com"

def test_get_me(client):
    # Signup and get token
    signup_res = client.post(
        "/auth/signup",
        json={
            "email": "me@example.com",
            "password": "password123",
            "full_name": "Me User"
        },
    )
    token = signup_res.json()["token"]
    
    # Get Me
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"
