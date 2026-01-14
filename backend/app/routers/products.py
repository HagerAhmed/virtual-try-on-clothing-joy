from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[schemas.Product])
async def get_products(
    category: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)
    if category and category != "All":
        query = query.filter(models.Product.category == category)
    
    return query.offset(offset).limit(limit).all()

@router.get("/{id}", response_model=schemas.Product)
async def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
