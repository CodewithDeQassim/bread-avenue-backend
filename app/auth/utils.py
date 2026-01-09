from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

SECRET_KEY = "I_am_supposed_change_this_later_to_a_random_secure_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTUES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashed_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire =datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTUES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
