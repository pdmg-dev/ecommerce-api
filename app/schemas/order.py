# app/schemas/order.py

from pydantic import BaseModel
from typing import List
from datetime import datetime

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
    created_at: datetime
    items: List[OrderItemRead]

    class Config:
        from_attributes = True