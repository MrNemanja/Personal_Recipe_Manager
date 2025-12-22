import os
from fastapi import Depends, HTTPException
from fastapi import Cookie
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import User
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire_time = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            return None
        else:
            return user_id
    except JWTError:
        return None

def get_current_user_optional(access_token: Optional[str] = Cookie(None), db: Session = Depends(get_db)) -> Optional[User]:
    
    print("Cookie token:", access_token)
    if not access_token:
        return None

    if access_token.startswith("Bearer "):
        access_token = access_token[len("Bearer "):]
    print("Token after Bearer cut:", access_token)

    user_id = verify_access_token(access_token)
    print("Decoded user_id:", user_id)
    if not user_id:
        return None

    user = db.query(User).filter(User.id == user_id).first()
    print("Fetched user:", user)
    return user

def get_current_user(access_token: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if access_token.startswith("Bearer "):
        access_token = access_token[len("Bearer "):]
    
    user_id = verify_access_token(access_token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
