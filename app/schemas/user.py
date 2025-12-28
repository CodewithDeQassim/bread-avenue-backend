from pydantic import BaseModel, EmailStr

#Request Schema(when creating a new user)
class UserCreate(BaseModel):
    username:str
    email: EmailStr
    password: str

#response Schema (when returning user data, e.g., in API responses)
class UserResponses(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes =True
