from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models import Cart, CartItem, Product, User, CartItemCreate, WishlistItemCreate
from ..database import carts, wishlists, products
from .auth import get_current_user

router = APIRouter(tags=["Cart", "Wishlist"])

# Cart Endpoints
@router.get("/cart", response_model=Cart)
async def get_cart(current_user: User = Depends(get_current_user)):
    if current_user.id not in carts:
        carts[current_user.id] = Cart(id=current_user.id, items=[], total=0.0)
    return carts[current_user.id]

@router.post("/cart/items", response_model=Cart)
async def add_to_cart(item: CartItemCreate, current_user: User = Depends(get_current_user)):
    cart = carts.get(current_user.id)
    if not cart:
        cart = Cart(id=current_user.id, items=[], total=0.0)
        carts[current_user.id] = cart
    
    product = next((p for p in products if p.id == item.product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if item exists
    existing_item = next(
        (i for i in cart.items 
         if i.product.id == item.product_id 
         and i.size == item.size 
         and i.color == item.color), 
        None
    )
    
    if existing_item:
        existing_item.quantity += item.quantity
    else:
        new_item = CartItem(
            id=len(cart.items) + 1, # Simple ID generation
            product=product,
            quantity=item.quantity,
            size=item.size,
            color=item.color
        )
        cart.items.append(new_item)
    
    # Recalculate total
    cart.total = sum(i.product.price * i.quantity for i in cart.items)
    
    return cart

@router.delete("/cart/items/{item_id}", response_model=Cart)
async def remove_from_cart(item_id: int, current_user: User = Depends(get_current_user)):
    cart = carts.get(current_user.id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    cart.items = [i for i in cart.items if i.id != item_id]
    cart.total = sum(i.product.price * i.quantity for i in cart.items)
    return cart

# Wishlist Endpoints
@router.get("/wishlist", response_model=List[Product])
async def get_wishlist(current_user: User = Depends(get_current_user)):
    return wishlists.get(current_user.id, [])

@router.post("/wishlist/items")
async def add_to_wishlist(item: WishlistItemCreate, current_user: User = Depends(get_current_user)):
    if current_user.id not in wishlists:
        wishlists[current_user.id] = []
    
    wishlist = wishlists[current_user.id]
    
    # Check if already in wishlist
    if any(p.id == item.product_id for p in wishlist):
        return {"message": "Product already in wishlist"}

    product = next((p for p in products if p.id == item.product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
        
    wishlist.append(product)
    return {"message": "Product added to wishlist"}

@router.delete("/wishlist/items/{product_id}")
async def remove_from_wishlist(product_id: int, current_user: User = Depends(get_current_user)):
    if current_user.id not in wishlists:
        return {"message": "Wishlist is empty"}
    
    wishlists[current_user.id] = [p for p in wishlists[current_user.id] if p.id != product_id]
    return {"message": "Product removed from wishlist"}
