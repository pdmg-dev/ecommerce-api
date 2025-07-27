import stripe
from app.core.settings import get_settings
from app.models.user import User
from app.repositories.cart_item import CartItemRepository
from app.utils.exception import Exception

settings = get_settings()
stripe.api_key = settings.stripe_secret_key

class PaymentService:
    def __init__(self, db):
        self.db = db

    def create_checkout_session(self, user: User):
        cart_repo = CartItemRepository(self.db)
        cart_items = cart_repo.get_user_cart_items(user.id)

        if not cart_items:
            raise Exception.bad_request("Cart is empty")

        line_items = [
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": item.product.name},
                    "unit_amount": int(item.product.price * 100),  # in cents
                },
                "quantity": item.quantity,
            }
            for item in cart_items
        ]

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            # success_url=f"{settings.frontend_domain}/success?session_id={{CHECKOUT_SESSION_ID}}",
            # cancel_url=f"{settings.frontend_domain}/cancel",
            success_url="http://localhost:8000/payment/success",
            cancel_url="http://localhost:8000/payment/cancel",
            metadata={"user_id": str(user.id)}
        )

        return {"checkout_url": session.url}
