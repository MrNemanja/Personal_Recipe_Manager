from models import User
from database import SessionLocal
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_admin():
    db = SessionLocal()
    try:
        admin_username = os.getenv("ADMIN_USERNAME")
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")

        existing_admin = db.query(User).filter(User.username == admin_username).first()
        if not existing_admin:
            hashed_password = pwd_context.hash(admin_password)
            admin_user = User(
                username=admin_username,
                password_hash=hashed_password,
                email=admin_email,
                role="admin",
                favorite_recipe_id=None
            )
            db.add(admin_user)
            db.commit()
            print("Admin user created")
        else:
            print("Admin user already exists")
    finally:
        db.close()