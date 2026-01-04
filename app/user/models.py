from sqlalchemy import Column, Integer, String
from ..database import Base

class User(Base):
    __tablename__= "users" #This is the name of the actual table in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key (Unique ID)
    username = Column(String, unique=True, index=True, nullable=False) # Unique username
    email = Column(String, unique=True, index=True, nullable=False) # Unique email
    full_name = Column(String, nullable=True) # Optional fullname
    hashed_password = Column(String, nullable=False) # password (hashed)
