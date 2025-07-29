# app/api/order.py
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_admin
from app.models.user import User
from app.schemas.order import OrderRead, OrderUpdateStatus
from app.services.order import OrderService
from app.core.dependencies import get_order_service

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/", response_model=List[OrderRead], status_code=status.HTTP_200_OK)
def list_orders(
    order_service: OrderService = Depends(get_order_service),
    current_user: User = Depends(get_current_user)
):
    return order_service.list_orders(current_user.id)

@router.get("/all", response_model=List[OrderRead])
def get_all_orders(
    order_service: OrderService = Depends(get_order_service),
    current_user: User = Depends(require_admin),
):
    return order_service.list_all_orders()


#@router.patch("/{order_id}", response_model=OrderRead)
#def update_order_status(
#    order_id: int,
    #status_data: OrderUpdateStatus,
    #db: Session = Depends(get_db),
    #current_user: User = Depends(require_admin),
#):
    
    #service = OrderService(db)
    #return service.change_order_status(order_id, status_data.status)
