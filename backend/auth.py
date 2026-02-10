import os
from fastapi import Depends, HTTPException
from fastapi import Cookie
from sqlalchemy.orm import Session
from database import get_db
from models import User, RefreshToken
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import secrets

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

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

def create_refresh_token(user: User, db: Session):

    token_str = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    refresh_token = RefreshToken(
        user_id = user.id,
        token=token_str,
        expires_at=expires_at
    )

    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)

    return token_str

def delete_expired_refresh_tokens(db: Session):

    db.query(RefreshToken).filter(RefreshToken.expires_at < datetime.utcnow()).delete()
    db.commit()


def get_current_user_optional(access_token: Optional[str] = Cookie(None), db: Session = Depends(get_db)) -> Optional[User]:
    
    if not access_token:
        return None

    if access_token.startswith("Bearer "):
        access_token = access_token[len("Bearer "):]

    user_id = verify_access_token(access_token)

    if not user_id:
        return None

    user = db.query(User).filter(User.id == user_id).first()

    if not user or not user.is_verified:
        return None

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
