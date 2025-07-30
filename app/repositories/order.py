# app/repositories/order.py

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cart_item import CartItem
from app.models.order import Order, OrderItem


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_order(self, user_id: int):
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
        )
        return self.db.scalars(stmt).all()

    def get_by_id(self, order_id: int):
        stmt = select(Order).where(Order.id == order_id)
        return self.db.scalars(stmt).one_or_none()

    def get_all_orders(self):
        stmt = select(Order).order_by(Order.created_at.desc())
        return self.db.scalars(stmt).all()

    def create_order(self, order: Order) -> Order:
        self.db.add(order)
        self.db.flush()
        return order

    def add_items(self, order_item: OrderItem) -> None:
        return self.db.add(order_item)

    def commit(self):
        self.db.commit()

    def refresh(self, instance):
        self.db.refresh(instance)

    def update_status(self, order: Order) -> Order:
        self.db.commit()
        self.db.refresh(order)
        return order
