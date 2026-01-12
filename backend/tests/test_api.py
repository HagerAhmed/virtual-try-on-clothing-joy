from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Virtual Wardrobe API"}

def test_auth_flow():
    # Signup
    signup_data = {
        "email": "test@example.com",
        "password": "Password123!",
        "full_name": "Test User"
    }
    response = client.post("/auth/signup", json=signup_data)
    assert response.status_code == 201
    data = response.json()
    assert "token" in data
    assert data["user"]["email"] == signup_data["email"]
    
    # Login
    login_data = {
        "email": "test@example.com",
        "password": "Password123!"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    assert "token" in response.json()

def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_cart_flow():
    # Helper to get auth token
    login_data = {
        "email": "test@example.com",
        "password": "Password123!"
    }
    # Ensure user exists (might fail if run out of order, but sequential usually ok)
    # Better to signup a fresh user for this test
    signup_data = {
        "email": "cartuser@example.com",
        "password": "Password123!",
        "full_name": "Cart User"
    }
    client.post("/auth/signup", json=signup_data)
    
    login_res = client.post("/auth/login", json={"email": "cartuser@example.com", "password": "Password123!"})
    token = login_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Add to cart
    item_data = {
        "product_id": 1,
        "quantity": 2,
        "size": "M",
        "color": "Blue"
    }
    response = client.post("/cart/items", json=item_data, headers=headers)
    assert response.status_code == 200
    cart = response.json()
    assert len(cart["items"]) == 1
    assert cart["items"][0]["quantity"] == 2
    
    # Get cart
    response = client.get("/cart", headers=headers)
    assert response.status_code == 200
    assert len(response.json()["items"]) == 1

def test_try_on():
    # Need to simulate file upload
    # Since it's a mock, we just check response structure
    
    files = {'userImage': ('test.jpg', b'fakeimagebytes', 'image/jpeg')}
    data = {'productId': '1'}
    
    response = client.post("/try-on/", data=data, files=files) 
    # Note: Using /try-on/ with trailing slash if router prefix doesn't match exactly without it? 
    # Router prefix is "/try-on". Function is check path.
    # Check router implementation: prefix="/try-on", path="/" -> "/try-on/"
    
    assert response.status_code == 200
    assert "result_image" in response.json()
