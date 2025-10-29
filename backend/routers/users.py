from fastapi import APIRouter, Path, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import CreateUser, UserResponse
from passlib.context import CryptContext

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=UserResponse)
def register_User(user: CreateUser, db: Session = Depends(get_db)):
    if db.query(User).filter((User.username == user.username) | (User.email == user.email)).first():
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(user.password)

    new_user = User(username=user.username, password_hash=hashed_password, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



