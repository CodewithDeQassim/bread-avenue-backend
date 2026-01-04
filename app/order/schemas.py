# app/order/schemas.py
from pydantic import BaseModel, EmailStr

class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    address: str | None = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None

class CustomerOut(CustomerBase):
    id: int

    class Config:
        from_attributes = True

class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: float
    price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(BaseModel):
    quantity: float | None = None
    price: float | None = None

class OrderItemOut(OrderItemBase):
    id: int

    class Config:
        from_attributes = True