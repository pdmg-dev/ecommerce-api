import os

import stripe
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from stripe import error

from app.core.dependencies import get_current_user, get_db
from app.core.settings import get_settings
from app.models.user import User
from app.services.order import OrderService
from app.services.payment import PaymentService
from app.utils import exceptions

router = APIRouter(prefix="/payment", tags=["Payment"])


# Load keys

settings = get_settings()
stripe.api_key = settings.stripe_secret_key
endpoint_secret = settings.stripe_webhook_secret


@router.post("/checkout")
def create_checkout_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PaymentService(db)
    return service.create_checkout_session(current_user)


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=endpoint_secret
        )
    except error.SignatureVerificationError:
        raise exceptions.bad_request("Invalid signature")

    # Handle successful payment
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = int(session["metadata"]["user_id"])

        service = OrderService(db)
        service.create_order_from_cart(user_id)

    return {"status": "ok"}


@router.get("/success", response_class=HTMLResponse)
def payment_success():
    return "<h1>Payment Successful</h1><p>Thank you for your purchase.</p>"


@router.get("/cancel", response_class=HTMLResponse)
def payment_cancel():
    return "<h1>Payment Canceled</h1><p>Your payment was canceled.</p>"
