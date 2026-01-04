from pydantic import BaseModel, EmailStr, Field
from typing import Optional

#Request Schema(when creating a new user)
class UserCreate(BaseModel):
    username:str
    email: EmailStr
    password: str=Field(min_length=8, max_length=64)  
    
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=64)

#response Schema (when returning user data, e.g., in API responses)
class UserResponses(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes =True
