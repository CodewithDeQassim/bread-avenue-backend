from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session



from .models import Order, OrderItem
from .schemas import OrderCreate, OrderOut
from app.product.models import Product
from app.user.models import User
from ..database import get_db
from app.auth.jwt import get_current_user
from app.auth.dependencies import require_role
from app.auth.roles import Roles

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


@router.get("/my-orders", dependencies=[Depends(require_role("customer"))])
def ge_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(Roles.CUSTOMER)),
):
    return (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .all()
    )

@router.patch("{order_id}/status", dependencies=[Depends(require_role("staff", "admin"))], response_model=OrderOut)
def update_order_status(
    order_id: int,
    status: str,
    staff = Depends(require_role(Roles.STAFF, Roles.ADMIN)),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(404, "Order not found")
    
    order.status = status
    db.commit()
    return order

@router.get("/all", dependencies=[Depends(require_role("staff", "admin"))], response_model=list[OrderOut])
def get_all_orders(
    admin = Depends(require_role(Roles.ADMIN)),
    db: Session = Depends(get_db)
):
    return db.query(Order).all()