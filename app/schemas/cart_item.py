# app/schemas/cart_item.py

from typing import Optional

from pydantic import BaseModel

from app.schemas.product import ProductRead


class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    quantity: int

class CartItemRead(BaseModel):
    id: int
    product: ProductRead
    quantity: int

    class Config:
        from_attributes = True
