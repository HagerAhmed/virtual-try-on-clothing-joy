from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, JSON, Table
from sqlalchemy.orm import relationship
from .database import Base

# Association table for Wishlist (User <-> Product)
wishlist_table = Table(
    'wishlist',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)

    cart = relationship("Cart", back_populates="user", uselist=False)
    wishlist = relationship("Product", secondary=wishlist_table)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    brand = Column(String)
    price = Column(Float)
    image = Column(String)
    category = Column(String, index=True)
    description = Column(String)
    
    # Store lists as JSON
    colors = Column(JSON)
    sizes = Column(JSON)
    details = Column(JSON)

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total = Column(Float, default=0.0)

    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    size = Column(String)
    color = Column(String)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")
