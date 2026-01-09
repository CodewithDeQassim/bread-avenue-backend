 # app/main.py
from fastapi import FastAPI
from app.database import engine, Base

from app.auth.routes import router as auth_router
from app.user.routes import router as user_router
from app.product.routes import router as product_router
from app.order.routes import router as order_router

#create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bread Avenue API", version="1.0.0")

app.include_router(auth_router, tags=["auth"])
app.include_router(user_router, tags=["users"])
app.include_router(product_router, tags=["products"])
app.include_router(order_router, tags=["orders"])   

@app.get("/")
def read_root():
     return {"message": "Welcome to Bread Avenue backend!"}
