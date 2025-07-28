# app/api/cart.py

from typing import List

from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_cart_service, get_current_user
from app.models.user import User
from app.schemas.cart_item import CartItemCreate, CartItemRead, CartItemUpdate
from app.services.cart import CartService

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/", response_model=List[CartItemRead], status_code=status.HTTP_200_OK)
def list_cart_items(
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_user),
):
    return cart_service.list_cart_items(current_user.id)


@router.post("/", response_model=CartItemRead, status_code=status.HTTP_201_CREATED)
def add_cart_item(
    create_data: CartItemCreate,
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_user),
):
    return cart_service.add_item(current_user.id, create_data)


@router.put(
    "/{product_id}", response_model=CartItemRead, status_code=status.HTTP_200_OK
)
def update_cart_item(
    product_id: int,
    update_data: CartItemUpdate,
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_user),
):
    return cart_service.update_item_quantity(
        current_user.id, product_id, update_data
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_cart_item(
    product_id: int,
    cart_service: CartService = Depends(get_cart_service),
    current_user: User = Depends(get_current_user),
):
    cart_service.remove_item(current_user.id, product_id)
    return 
