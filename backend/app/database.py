from typing import List, Dict, Optional
from .models import User, Product, Cart, CartItem, UserCreate

# Mock Data Storage
users: Dict[str, User] = {}  # email -> User
products: List[Product] = []
carts: Dict[int, Cart] = {} # user_id -> Cart
wishlists: Dict[int, List[Product]] = {} # user_id -> List[Product]

# Password hashing mock (simplified for now, usually handled in auth service)
# In a real app, 'hashed_password' would be stored.
user_passwords: Dict[str, str] = {} # email -> hashed_password

# Initialize some products
def init_products():
    from .models import Product
    # Using the same data as frontend/src/data/products.ts
    mock_products = [
      { 
        "id": 1, 
        "name": "Silk Button Blouse", 
        "brand": "Everlane", 
        "price": 128, 
        "image": "/assets/clothing-1.jpg", 
        "category": "Tops",
        "description": "Crafted from 100% mulberry silk...",
        "colors": ["Ivory", "Blush", "Navy"],
        "sizes": ["XS", "S", "M", "L", "XL"],
        "details": ["100% Mulberry Silk"]
      },
      { 
        "id": 2, 
        "name": "Tailored Camel Blazer", 
        "brand": "COS", 
        "price": 275, 
        "image": "/assets/clothing-2.jpg", 
        "category": "Outerwear",
        "description": "A modern take on the classic blazer...",
        "colors": ["Camel", "Black", "Charcoal"],
        "sizes": ["XS", "S", "M", "L", "XL"],
        "details": ["70% Wool, 30% Polyester"]
      },
      # Add more if needed, but this is enough strictly for dev
    ]
    for p in mock_products:
        products.append(Product(**p))

init_products()
