 # app/main.py
from fastapi import FastAPI
from app.routes import user, product
from app.models.user import User
from app.database import engine, Base

#create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(product.router)

@app.get("/")
def read_root():
     return {"message": "Welcome to Bread Avenue backend!"}
