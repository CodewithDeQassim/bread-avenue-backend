from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from fastapi.security import HTTPAuthorizationCredentials

from app.database import get_db
from app.user.models import User
from app.user.schemas import UserOut
from app.auth.security import bearer_scheme
from .schemas import LoginRequest
from .utils import ALGORITHM, verify_password, create_access_token, create_refresh_token, SECRET_KEY
from .jwt import get_current_user
from .models import RefreshToken

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

   
    access_token = create_access_token({"sub": str(user.id)})

    refresh_token, jti, expires = create_refresh_token(str(user.id))

    db_token = RefreshToken(
        jti=jti,
        user_id=user.id,
        expires_at=expires
    )

    db.add(db_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.post("/refresh")
def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    jti = payload.get("jti")
    user_id: str = payload.get("sub")

    db_token = db.query(RefreshToken).filter(
        RefreshToken.jti == jti,
        RefreshToken.revoked == False
    ).first()

    if not db_token:
        raise HTTPException(status_code=401, detail="Refresh token has been revoked")
    
    # ROTATION: Revoke old token
    db_token.revoked = True

    # Issue new tokens
    new_access_token = create_access_token({"sub": user_id})
    new_refresh_token, new_jti, expires = create_refresh_token(user_id)

    db.add(
        RefreshToken(
            jti=new_jti,
            user_id=int(user_id),
            expires_at=expires
        )
    )

    db.commit()

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }

@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
): 
    token = credentials.credentials

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    jti = payload.get("jti")

    if not jti:
        raise HTTPException(status_code=400, detail="Invalid token")

    db_token = db.query(RefreshToken).filter(
        RefreshToken.jti == jti,
        RefreshToken.revoked == False
    ).first()
    
    if db_token:
        db_token.revoked = True
        db.commit()

    return {"message": "Logged out successfully"}

@router.post("/logout_all")
def logout_all(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(RefreshToken).filter(
        RefreshToken.user_id == current_user.id, 
        RefreshToken.revoked == False
    ).update({"revoked": True})

    db.commit()
    return {"detail": "Logged out from all devices successfully"}



#creating another protected endpoint to test the authorization
@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/_auth_check")
def auth_check(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    return {"ok": True}