# app/services/order.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.cart_item import CartItem
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.repositories.order import OrderRepository


class OrderService:
    def __init__(self, db: Session):
        self.repo = OrderRepository(db)
        self.db = db
        
    def get_user_orders(self, user_id: int):
        return self.repo.get_orders_by_user(user_id)


    def checkout(self, user_id: int):
        cart_items = self.repo.get_user_cart_items(user_id)
        if not cart_items:
            raise ValueError("Cart is empty.")

        total = 0.0
        order_items = []

        for item in cart_items:
            product = self.repo.get_product_by_id(item.product_id)
            if not product or product.quantity < item.quantity:
                raise ValueError(f"Not enough stock for product ID {item.product_id}.")

            total += product.price * item.quantity

            # Decrease product stock
            product.quantity -= item.quantity

            order_items.append(OrderItem(
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=product.price
            ))

        # Create order
        order = self.repo.create_order(user_id, total, order_items)

        # Clear cart
        self.repo.remove_user_cart(user_id)
        self.repo.commit()
        self.repo.refresh(order)
        return order

    def list_all_orders(self):
        return self.repo.get_all_orders()

    def change_order_status(self, order_id: int, new_status: OrderStatus):
        order = self.repo.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        order.status = new_status
        return self.repo.update_order_status(order)