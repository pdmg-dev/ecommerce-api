# app/services/payment.py
from typing import Any, Dict

import stripe
from stripe import StripeError, checkout

from app.core.settings import get_settings
from app.models.user import User
from app.repositories.cart import CartRepository
from app.utils import exceptions

settings = get_settings()


class PaymentService:
    def __init__(self, cart_repository: CartRepository) -> None:
        self.cart_repository = cart_repository

    def configure_stripe(self) -> None:
        stripe.api_key = settings.stripe_secret_key

    def create_checkout_session(self, user: User) -> Dict[str, Any]:
        self.configure_stripe()

        cart_items = self.cart_repository.get_all_items(user.id)
        if not cart_items:
            raise exceptions.bad_request("Cart is empty")

        line_items = [
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": item.product.name},
                    "unit_amount": int(item.product.price * 100),
                },
                "quantity": item.quantity,
            }
            for item in cart_items
        ]

        try:
            session = checkout.Session.create(
                payment_method_types=["card"],
                line_items=line_items,
                mode="payment",
                success_url=f"{settings.base_url}/payment/success",
                cancel_url=f"{settings.base_url}/payment/cancel",
                metadata={"user_id": str(user.id)},
            )
            return {"checkout_url": session.url}
        except StripeError as e:
            raise exceptions.bad_gateway(f"Stripe: {str(e)}")
