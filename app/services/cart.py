from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.cart_item import CartItem
from app.repositories.cart import CartRepository
from app.repositories.product import ProductRepository
from app.schemas.cart_item import CartItemCreate, CartItemUpdate
from app.utils import exceptions


class CartService:
    def __init__(
        self,
        cart_repository: CartRepository,
        product_repository: ProductRepository,
    ):
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    def list_cart_items(self, user_id: int):
        return self.cart_repository.get_all_items(user_id)

    def add_item(self, user_id: int, create_data: CartItemCreate):
        product = self.product_repository.get_by_id(create_data.product_id)
        if not product:
            raise exceptions.not_found("Product not found")
        if create_data.quantity > product.quantity:
            raise exceptions.bad_request("Quantity exceeds available stock")

        existing_item = self.cart_repository.get_item(user_id, product.id)
        if existing_item:
            new_quantity = existing_item.quantity + create_data.quantity
            if new_quantity > product.quantity:
                raise exceptions.bad_request("Quantity exceeds available stock")
            return self.cart_repository.update_quantity(existing_item, new_quantity)

        new_item = CartItem(
            user_id=user_id,
            product_id=create_data.product_id,
            quantity=create_data.quantity,
        )
        return self.cart_repository.add_item(new_item)

    def update_item_quantity(
        self, user_id: int, product_id: int, update_data: CartItemUpdate
    ):
        item = self.cart_repository.get_item(user_id, product_id)
        if not item:
            raise exceptions.not_found("Cart item not found")
        return self.cart_repository.update_quantity(item, update_data.quantity)

    def remove_item(self, user_id: int, product_id: int):
        item = self.cart_repository.get_item(user_id, product_id)
        if not item:
            raise exceptions.not_found("Cart item not found")
        return self.cart_repository.delete_item(item)
