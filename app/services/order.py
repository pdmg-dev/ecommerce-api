# app/services/order.py

from app.models.order import Order, OrderItem, OrderStatus
from app.repositories.cart import CartRepository
from app.repositories.order import OrderRepository
from app.utils import exceptions


class OrderService:
    def __init__(
        self, cart_repository: CartRepository, order_repository: OrderRepository
    ):
        self.cart_repository = cart_repository
        self.order_repository = order_repository

    def list_orders(self, user_id: int):
        return self.order_repository.get_order(user_id)

    def list_all_orders(self):
        return self.order_repository.get_all_orders()

    def update_order_status(self, order_id: int, new_status: OrderStatus):
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise exceptions.bad_request("Order not found")
        order.status = new_status
        return self.order_repository.update_status(order)

    def create_order(self, user_id: int) -> Order:
        cart_items = self.cart_repository.get_all_items(user_id)
        total_price = sum(item.quantity * item.product.price for item in cart_items)

        order = Order(user_id=user_id, total_price=total_price)
        saved_order = self.order_repository.create_order(order)

        for item in cart_items:
            order_item = OrderItem(
                order_id=saved_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=item.product.price,
            )
            self.order_repository.add_items(order_item)

        self.cart_repository.remove_all_items(user_id)
        self.order_repository.commit()
        return order
