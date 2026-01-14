from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from .auth import get_current_user

router = APIRouter(tags=["Cart", "Wishlist"])

# Cart Endpoints
@router.get("/cart", response_model=schemas.Cart)
async def get_cart(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.cart:
        new_cart = models.Cart(user_id=current_user.id)
        db.add(new_cart)
        db.commit()
        db.refresh(current_user)
    
    return current_user.cart

@router.post("/cart/items", response_model=schemas.Cart)
async def add_to_cart(
    item: schemas.CartItemCreate, 
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Ensure cart exists
    if not current_user.cart:
        new_cart = models.Cart(user_id=current_user.id)
        db.add(new_cart)
        db.commit()
        db.refresh(current_user)
    
    cart = current_user.cart

    # Check product
    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if item exists in cart
    existing_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart.id,
        models.CartItem.product_id == item.product_id,
        models.CartItem.size == item.size,
        models.CartItem.color == item.color
    ).first()
    
    if existing_item:
        existing_item.quantity += item.quantity
    else:
        new_item = models.CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=item.quantity,
            size=item.size,
            color=item.color
        )
        db.add(new_item)
    
    # Recalculate total
    # Need to flush to ensure items are up to date for calculation?
    # Or just calculate from what we have.
    # Since we modified existing or added new, let's commit first to be safe or calculate manually.
    # A cleaner way is to sum it up.
    
    db.commit() 
    db.refresh(cart)
    
    # Recalculate total based on DB state
    new_total = sum(i.product.price * i.quantity for i in cart.items)
    cart.total = new_total
    db.commit()
    db.refresh(cart)
    
    return cart

@router.delete("/cart/items/{item_id}", response_model=schemas.Cart)
async def remove_from_cart(
    item_id: int, 
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart = current_user.cart
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    item = db.query(models.CartItem).filter(models.CartItem.id == item_id, models.CartItem.cart_id == cart.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
        
    db.delete(item)
    db.commit()
    db.refresh(cart)
    
    # Recalculate total
    cart.total = sum(i.product.price * i.quantity for i in cart.items)
    db.commit()
    db.refresh(cart)

    return cart

# Wishlist Endpoints
@router.get("/wishlist", response_model=List[schemas.Product])
async def get_wishlist(current_user: models.User = Depends(get_current_user)):
    return current_user.wishlist

@router.post("/wishlist/items")
async def add_to_wishlist(
    item: schemas.WishlistItemCreate, 
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    if product in current_user.wishlist:
        return {"message": "Product already in wishlist"}
        
    current_user.wishlist.append(product)
    db.commit()
    
    return {"message": "Product added to wishlist"}

@router.delete("/wishlist/items/{product_id}")
async def remove_from_wishlist(
    product_id: int, 
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    product = next((p for p in current_user.wishlist if p.id == product_id), None)
    if not product:
         return {"message": "Product not in wishlist"} # Or 404
    
    current_user.wishlist.remove(product)
    db.commit()
    
    return {"message": "Product removed from wishlist"}
