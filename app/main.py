 # app/main.py
from fastapi import FastAPI
from app.database import engine, Base

from app.user.routes import router as router
from app.product.routes import router as product_router
#from app.order.routes import router as order_router

#create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bread Avenue API", version="1.0.0")

app.include_router(router, tags=["users"])
app.include_router(product_router, tags=["products"])
#app.include_router(order_router, prefix="/orders", tags=["orders"])   

@app.get("/")
def read_root():
     return {"message": "Welcome to Bread Avenue backend!"}
