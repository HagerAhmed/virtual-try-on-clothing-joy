from app import models

def test_add_to_cart(client, db):
    # 1. Create User & Token
    signup_res = client.post(
        "/auth/signup",
        json={
            "email": "cart@example.com",
            "password": "password123",
            "full_name": "Cart User"
        },
    )
    token = signup_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create Product (using DB directly as there is no API for it)
    product = models.Product(
        name="Test Shirt",
        brand="Test Brand",
        price=10.0,
        image="test.jpg",
        category="Tops",
        description="Test Desc",
        colors=["Red", "Blue"],
        sizes=["M", "L"],
        details=["Detail 1"]
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    
    # 3. Add to Cart
    res = client.post(
        "/cart/items",
        json={
            "product_id": product.id,
            "quantity": 2,
            "size": "M",
            "color": "Red"
        },
        headers=headers
    )
    assert res.status_code == 200
    data = res.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["product"]["name"] == "Test Shirt"
    assert data["items"][0]["quantity"] == 2
    assert data["total"] == 20.0

def test_remove_from_cart(client, db):
    # 1. Setup User
    signup_res = client.post(
        "/auth/signup",
        json={
            "email": "remove@example.com",
            "password": "password123",
            "full_name": "Remove User"
        },
    )
    token = signup_res.json()["token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Setup Product
    product = models.Product(
        name="Remove Shirt",
        brand="Brand",
        price=10.0,
        image="test.jpg",
        category="Tops",
        description="Desc",
        colors=["Red"],
        sizes=["M"],
        details=[]
    )
    db.add(product)
    db.commit()
    
    # 3. Add to Cart
    client.post(
        "/cart/items",
        json={
            "product_id": product.id,
            "quantity": 1,
            "size": "M",
            "color": "Red"
        },
        headers=headers
    )
    
    # Get Cart to find Item ID (since API doesn't return ID in add response nicely? actually it does)
    cart_res = client.get("/cart", headers=headers)
    item_id = cart_res.json()["items"][0]["id"]
    
    # 4. Remove Item
    del_res = client.delete(f"/cart/items/{item_id}", headers=headers)
    assert del_res.status_code == 200
    
    # 5. Verify Empty
    cart_final = client.get("/cart", headers=headers).json()
    assert len(cart_final["items"]) == 0
    assert cart_final["total"] == 0.0
