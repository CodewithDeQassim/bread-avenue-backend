from fastapi  import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models
from app .schemas.product import ProductCreate, ProductUpdate, ProductOut
from app.database import get_db

router = APIRouter(
prefix="/products",
    tags=["products"]
)
#creating a new product
@router.post("/", response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
#getting all products
@router.get("/", response_model=list[ProductOut])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()
# updating a product
@router.put("/{product_id}",response_model=list[ProductOut])
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    #Find the product by id
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not  db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    #update only the fields that are provided
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product

#deleting a product
@router.delete("/{product_id}", response_model=dict)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}