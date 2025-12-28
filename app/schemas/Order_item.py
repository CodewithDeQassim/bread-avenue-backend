#app/schemas/order_item.py
from pydantic import BaseModel

class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: float
    price: float

# schema for creating an order item (inherits from base)
class OrderItemCreate(OrderItemBase):
    pass

# Schema for updating an order item (all fields oop