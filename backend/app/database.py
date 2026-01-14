from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import json

# Default to SQLite for simplicity if POSTGRES_URL not provided
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
# For Postgres: 
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

check_same_thread = False
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    check_same_thread = True
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Seed data
def init_db(db):
    from . import models
    
    # Check if products exist
    if db.query(models.Product).first():
        return

    mock_products = [
      { 
        "id": 1, 
        "name": "Silk Button Blouse", 
        "brand": "Everlane", 
        "price": 128.0, 
        "image": "/assets/clothing-1.jpg", 
        "category": "Tops",
        "description": "Crafted from 100% mulberry silk, this relaxed-fit blouse features a subtle sheen that transitions effortlessly from office to evening. The covered button placket and soft collar create a polished, refined silhouette.",
        "colors": ["Ivory", "Blush", "Navy"],
        "sizes": ["XS", "S", "M", "L", "XL"],
        "details": ["100% Mulberry Silk", "Relaxed fit", "Covered button placket", "Dry clean only", "Imported"]
      },
      { 
        "id": 2, 
        "name": "Tailored Camel Blazer", 
        "brand": "COS", 
        "price": 275.0, 
        "image": "/assets/clothing-2.jpg", 
        "category": "Outerwear",
        "description": "A modern take on the classic blazer, featuring clean lines and a structured silhouette. Made from a premium wool blend that drapes beautifully while maintaining its shape throughout the day.",
        "colors": ["Camel", "Black", "Charcoal"],
        "sizes": ["XS", "S", "M", "L", "XL"],
        "details": ["70% Wool, 30% Polyester", "Tailored fit", "Single-breasted", "Interior pocket", "Dry clean recommended"]
      },
      { 
        "id": 3, 
        "name": "Flowing Midi Dress", 
        "brand": "Reformation", 
        "price": 198.0, 
        "image": "/assets/clothing-3.jpg", 
        "category": "Dresses",
        "description": "This effortlessly elegant midi dress features a flattering A-line silhouette that moves gracefully with every step. Perfect for warm-weather occasions or layered under a blazer for cooler months.",
        "colors": ["Terracotta", "Sage", "Cream"],
        "sizes": ["XS", "S", "M", "L", "XL"],
        "details": ["100% Viscose", "A-line silhouette", "Hidden back zipper", "Midi length", "Machine washable"]
      },
      { 
        "id": 4, 
        "name": "Wide-Leg Trousers", 
        "brand": "Theory", 
        "price": 245.0, 
        "image": "/assets/clothing-4.jpg", 
        "category": "Bottoms",
        "description": "Sophisticated wide-leg trousers crafted from a premium stretch wool blend. The high waist and flowing silhouette create an elongating effect, while the tailored details ensure a polished finish.",
        "colors": ["Black", "Navy", "Cream"],
        "sizes": ["0", "2", "4", "6", "8", "10", "12"],
        "details": ["96% Wool, 4% Elastane", "High-rise", "Wide-leg fit", "Side zip closure", "Dry clean only"]
      },
      { 
        "id": 5, 
        "name": "Cashmere Ribbed Sweater", 
        "brand": "Vince", 
        "price": 365.0, 
        "image": "/assets/clothing-5.jpg", 
        "category": "Tops",
        "description": "Luxuriously soft cashmere sweater with a classic ribbed texture. The relaxed fit and slightly oversized silhouette make it perfect for layering or wearing on its own.",
        "colors": ["Oatmeal", "Heather Grey", "Camel"],
        "sizes": ["XS", "S", "M", "L", "XL"],
        "details": ["100% Cashmere", "Relaxed fit", "Ribbed texture", "Crew neckline", "Hand wash or dry clean"]
      },
      { 
        "id": 6, 
        "name": "Pleated Maxi Skirt", 
        "brand": "Aritzia", 
        "price": 168.0, 
        "image": "/assets/clothing-6.jpg", 
        "category": "Bottoms",
        "description": "Elegant pleated maxi skirt that adds movement and drama to any outfit. The flowing silhouette and high waist create a universally flattering fit.",
        "colors": ["Champagne", "Black", "Dusty Rose"],
        "sizes": ["XS", "S", "M", "L", "XL"],
        "details": ["100% Polyester", "High-waisted", "Accordion pleats", "Elasticized waistband", "Machine washable"]
      },
      { 
        "id": 7, 
        "name": "Leather Tote Bag", 
        "brand": "Mansur Gavriel", 
        "price": 495.0, 
        "image": "/assets/accessory-1.jpg", 
        "category": "Accessories",
        "description": "Timeless leather tote crafted from vegetable-tanned Italian leather. Spacious interior with contrast lining, perfect for work or weekend adventures.",
        "colors": ["Tan", "Black", "Burgundy"],
        "sizes": ["One Size"],
        "details": ["100% Italian Vegetable-Tanned Leather", "Cotton canvas lining", "Interior zip pocket", "Dimensions: 15\"W x 12\"H x 6\"D"]
      },
      { 
        "id": 8, 
        "name": "Silk Neck Scarf", 
        "brand": "Totême", 
        "price": 145.0, 
        "image": "/assets/accessory-2.jpg", 
        "category": "Accessories",
        "description": "Versatile silk scarf in a signature print, perfect for adding a touch of elegance to any ensemble. Wear it around your neck, in your hair, or tied to your favorite bag.",
        "colors": ["Print", "Solid Ivory", "Solid Black"],
        "sizes": ["One Size"],
        "details": ["100% Silk twill", "Hand-rolled edges", "Dimensions: 35\" x 35\"", "Dry clean only"]
      },
      { 
        "id": 9, 
        "name": "Gold Circle Jewelry Set", 
        "brand": "Mejuri", 
        "price": 225.0, 
        "image": "/assets/accessory-3.jpg", 
        "category": "Accessories",
        "description": "Minimalist jewelry set featuring delicate gold vermeil pieces. Includes hoop earrings, pendant necklace, and stackable ring for effortless everyday elegance.",
        "colors": ["Gold", "Silver", "Rose Gold"],
        "sizes": ["Ring sizes: 5, 6, 7, 8"],
        "details": ["18k Gold Vermeil", "Sterling silver base", "Hypoallergenic", "Tarnish-resistant coating"]
      },
    ]

    for p in mock_products:
        db_product = models.Product(**p)
        db.add(db_product)
    
    db.commit()
