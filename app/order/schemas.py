# app/order/schemas.py
from pydantic import BaseModel 
from typing import List

# Schemas for Order Items
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    

class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


# Schemas for Orders
class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderOut(BaseModel):
    id: int
    status: str
    total_amount: float
    items: List[OrderItemOut]

    class Config:
        from_attributes = True