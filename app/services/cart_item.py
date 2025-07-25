from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.cart_item import CartItem
from app.repositories.cart_item import CartItemRepository
from app.repositories.product import ProductRepository
from app.schemas.cart_item import CartItemCreate, CartItemUpdate


class CartItemService:
    def __init__(self, db: Session):
        self.repo = CartItemRepository(db)
        self.product_repo = ProductRepository(db)

    def list_user_cart(self, user_id: int):
        return self.repo.get_user_cart_items(user_id)

    def add_to_cart(self, user_id: int, data: CartItemCreate):
        product = self.product_repo.get_by_id(data.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        existing = self.repo.get_cart_item(user_id, data.product_id)
        if existing:
            # If already in cart, update quantity
            new_quantity = existing.quantity + data.quantity
            return self.repo.update_quantity(existing, new_quantity)

        new_item = CartItem(
            user_id=user_id,
            product_id=data.product_id,
            quantity=data.quantity,
        )
        return self.repo.add_cart_item(new_item)

    def update_cart_item(self, user_id: int, product_id: int, data: CartItemUpdate):
        item = self.repo.get_cart_item(user_id, product_id)
        if not item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        return self.repo.update_quantity(item, data.quantity)

    def remove_from_cart(self, user_id: int, product_id: int):
        item = self.repo.get_cart_item(user_id, product_id)
        if not item:
            raise HTTPException(status_code=404, detail="Cart item not found")
        self.repo.delete_item(item)
