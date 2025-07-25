# app/api/order.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.order import OrderRead
from app.services.order import OrderService

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
    
    
@router.get("/", response_model=List[OrderRead])
def list_user_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = OrderService(db)
    return service.get_user_orders(current_user.id)