from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Boolean
from ..database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__= "users" #This is the name of the actual table in the database

    id = Column(Integer, primary_key=True, index=True) # Primary Key (Unique ID)
    username = Column(String, unique=True, index=True, nullable=False) # Unique username
    email = Column(String, unique=True, index=True, nullable=False) # Unique email
    full_name = Column(String, nullable=True) # Optional fullname
    hashed_password = Column(String, nullable=False) # password (hashed)
    role = Column(String,default="customer", nullable=False) # user role

    orders = relationship("Order", back_populates="user", cascade="all, delete")


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    refresh_token = Column(String, unique=True, nullable=False)
    user_agent = Column(String)
    ip_address = Column(String)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)