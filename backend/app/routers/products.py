from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..models import Product
from ..database import products

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[Product])
async def get_products(
    category: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
):
    result = products
    if category and category != "All":
        result = [p for p in products if p.category == category]
    
    return result[offset : offset + limit]

@router.get("/{id}", response_model=Product)
async def get_product(id: int):
    product = next((p for p in products if p.id == id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
