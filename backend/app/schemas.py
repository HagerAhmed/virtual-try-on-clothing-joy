from pydantic import BaseModel, EmailStr
from typing import List, Optional

# User Models
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True

# Token Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class AuthResponse(BaseModel):
    token: str
    user: User

# Product Models
class Product(BaseModel):
    id: int
    name: str
    brand: str
    price: float
    image: str
    category: str
    description: str
    colors: List[str]
    sizes: List[str]
    details: List[str]

# Cart Models
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1
    size: str
    color: str

class CartItem(BaseModel):
    id: int
    product: Product
    quantity: int
    size: str
    color: str

class Cart(BaseModel):
    id: int
    items: List[CartItem]
    total: float

# Wishlist Models
class WishlistItemCreate(BaseModel):
    product_id: int

# Try On Models
class TryOnResult(BaseModel):
    result_image: str
