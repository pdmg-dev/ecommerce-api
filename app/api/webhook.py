# app/app/webhook.py

from fastapi import APIRouter, Request
from stripe import SignatureVerificationError, Webhook

from app.core.settings import get_settings
from app.utils import exceptions

router = APIRouter(prefix="/webhook", tags=["Webhook"])


settings = get_settings()


@router.post("/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except SignatureVerificationError:
        raise exceptions.bad_request("Invalid signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = int(session["metadata"]["user_id"])

    return {"status": "success"}
