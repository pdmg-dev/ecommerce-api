# app/app/webhook.py

from fastapi import APIRouter, Request, Depends
from stripe import Webhook, SignatureVerificationError
from app.core.settings import get_settings
from app.utils import exceptions
from app.services.order import OrderService
from app.core.dependencies import get_order_service

router = APIRouter(prefix="/webhook", tags=["Webhook"])


settings = get_settings()


@router.post("/stripe")
async def stripe_webhook(
    request: Request, order_service: OrderService = Depends(get_order_service)
):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            user_id = int(session["metadata"]["user_id"])
            return order_service.create_order(user_id)

    except SignatureVerificationError:
        raise exceptions.bad_request("Invalid signature")
    except Exception as e:
        print(f"Webhook error: {e}")
        raise exceptions.internal_server_error("Webhook processing failed")

    return {"status": "success"}
