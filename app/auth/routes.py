from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database import get_db
from app.user.models import User
from .schemas import TokenResponse
from .utils import verify_password, create_access_token
from .dependencies import get_current_user
from .dependencies import oauth2_scheme

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

#creating another protected endpoint to test the athorizaion
@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/_auth_check")
def auth_check(token: str = Depends(oauth2_scheme)):
    return {"ok": True}