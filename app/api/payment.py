from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from app.core.dependencies import get_current_user, get_payment_service
from app.models.user import User
from app.services.payment import PaymentService

router = APIRouter(prefix="/payment", tags=["Payment"])


@router.post("/checkout")
def checkout(
    payment_service: PaymentService = Depends(get_payment_service),
    current_user: User = Depends(get_current_user),
):
    return payment_service.create_checkout_session(current_user)


@router.get("/success", response_class=HTMLResponse)
def payment_success():
    return HTMLResponse("<h1>✅ Payment Successful</h1>")


@router.get("/cancel", response_class=HTMLResponse)
def payment_cancel():
    return HTMLResponse("<h1>❌ Payment Cancelled</h1></p>")
