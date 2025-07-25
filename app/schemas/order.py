# app/schemas/order.py
from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel


class OrderStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: float


class OrderItemRead(OrderItemBase):
    id: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    total_price: float
    status: str = "pending"


class OrderRead(OrderBase):
    id: int
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemRead]

    class Config:
        from_attributes = True


class OrderUpdateStatus(BaseModel):
    status: OrderStatus
