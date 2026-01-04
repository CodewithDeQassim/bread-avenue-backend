from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate, UserResponses, UserUpdate
from ..database import get_db
from passlib.context import CryptContext


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

#password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#Utility function to hash passwords
def hash_password(password:str):
    return pwd_context.hash(password)


# Create a new user (Registration)
@router.post("/", response_model=UserResponses)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    #check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_pw = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


#get all users
@router.get("/", response_model=list[UserResponses])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()


#get user by ID
@router.get("/{user_id}", response_model=UserResponses)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
#update user
@router.put("/{user_id}", response_model=UserResponses)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.username is not None:
        db_user.username = user.username

    if user.email is not None:
        db_user.email = user.email

    if user.password is not None:    
        db_user.hashed_password = hash_password(user.password)

    db.commit()
    db.refresh(db_user)
    return db_user
#delete user
@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted successfully"}
