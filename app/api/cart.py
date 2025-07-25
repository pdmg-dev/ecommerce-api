# app/api/cart.py

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.cart_item import CartItemCreate, CartItemRead, CartItemUpdate
from app.services.cart_item import CartItemService

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/", response_model=List[CartItemRead])
def get_cart_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = CartItemService(db)
    return service.list_user_cart(current_user.id)

@router.post("/", response_model=CartItemRead, status_code=201)
def add_cart_item(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = CartItemService(db)
    return service.add_to_cart(current_user.id, item)

@router.put("/{product_id}", response_model=CartItemRead)
def update_cart_item(
    product_id: int,
    item: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = CartItemService(db)
    return service.update_cart_item(current_user.id, product_id, item)

@router.delete("/{product_id}", status_code=204)
def remove_cart_item(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = CartItemService(db)
    service.remove_from_cart(current_user.id, product_id)
    return
