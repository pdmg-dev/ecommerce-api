# app/api/order.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_user
from app.services.order import OrderService
from app.schemas.order import OrderRead
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/checkout", response_model=OrderRead)
def checkout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = OrderService(db)
    try:
        return service.checkout(current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
