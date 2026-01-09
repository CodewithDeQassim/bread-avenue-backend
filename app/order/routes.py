from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .models import Order, OrderItem
from .schemas import OrderCreate, OrderOut
from app.product.models import Product
from app.user.models import User
from ..database import get_db
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

@router.post("/", response_model=OrderOut)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total_amount = 0.0
    order_items = []

    for item in order.items:
        if item.quantity <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be greater than zero")
        
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        total_amount += product.price * item.quantity

        order_items.append(
            OrderItem(
                product_id=product.id,
                quantity=item.quantity,
                price=product.price
            )
        )

    new_order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        items=order_items
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@router.get("/", response_model=list[OrderOut])
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    orders = (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .all()
    )
    return orders

@router.get("/my-orders", response_model=list[OrderOut])
def ge_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .all()
    )