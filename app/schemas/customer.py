#app/schemas/customer.py
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