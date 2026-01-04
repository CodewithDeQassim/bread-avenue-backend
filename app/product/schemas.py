#app/schemas/product.py
from pydantic import BaseModel
from typing import Optional
#common fields shared by all product operations
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None

#schemas for creating a new product
class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None

class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True
