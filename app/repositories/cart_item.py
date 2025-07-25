# app/repositories/cart_item.py

from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update
from app.models.cart_item import CartItem

class CartItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_cart_items(self, user_id: int):
        stmt = select(CartItem).where(CartItem.user_id == user_id)
        return self.db.scalars(stmt).all()

    def get_cart_item(self, user_id: int, product_id: int):
        stmt = select(CartItem).where(
            CartItem.user_id == user_id,
            CartItem.product_id == product_id
        )
        return self.db.scalar(stmt)

    def add_cart_item(self, item: CartItem):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update_quantity(self, item: CartItem, new_quantity: int):
        item.quantity = new_quantity
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete_item(self, item: CartItem):
        self.db.delete(item)
        self.db.commit()
