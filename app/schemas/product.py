#app/schemas/product.py
from pydantic import BaseModel

#common fields shared by all product operations
class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    image_url: str | None = None

#schemas for creating a new product
class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float |None = None
    image_url: str | None = None

class ProductOut(BaseModel):
    id: int

    class Config:
        from_attributes = True
