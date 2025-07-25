# app/repositories/order.py

from sqlalchemy.orm import Session

from app.models.cart_item import CartItem
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_cart_items(self, user_id: int):
        return self.db.query(CartItem).filter_by(user_id=user_id).all()

    def get_product_by_id(self, product_id: int):
        return self.db.query(Product).filter_by(id=product_id).first()
    
    
    def get_orders_by_user(self, user_id: int):
        return self.db.query(Order).filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    
    def get_all_orders(self):
        return self.db.query(Order).order_by(Order.created_at.desc()).all()

    def create_order(self, user_id: int, total_price: float, items: list[OrderItem]):
        order = Order(user_id=user_id, total_price=total_price, items=items)
        self.db.add(order)
        return order

    def remove_user_cart(self, user_id: int):
        self.db.query(CartItem).filter_by(user_id=user_id).delete()

    def commit(self):
        self.db.commit()

    def refresh(self, instance):
        self.db.refresh(instance)
        
    def get_order_by_id(self, order_id: int) -> Order:
        return self.db.query(Order).filter_by(id=order_id).first()
        
    def update_order_status(self, order: Order) -> Order:
        self.db.commit()
        self.db.refresh(order)
        return order
