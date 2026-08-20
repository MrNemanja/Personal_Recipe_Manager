from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey, Enum, UniqueConstraint, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from database import Base
import enum

user_favorites = Table (
    "user_favorites",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("recipe_id", Integer, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True)
)

# Recipe model: stores recipe details
class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    recipe_name = Column(String, index=True, unique=True, nullable=False)
    recipe_ingredients = Column(JSONB, nullable=False)
    preperation_time = Column(Integer, nullable=False)
    dish_type = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    image_url = Column(String, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"))
    recipe_owner = relationship("User", back_populates="owned_recipes", foreign_keys=[owner_id])

    favorited_by = relationship("User", secondary=user_favorites, back_populates="favorite_recipes")

# Role types
class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"


# User model: stores user details
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    full_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    city = Column(String, nullable=True)
    country = Column(String, nullable=True)
    dob = Column(Date, nullable=True)
    profile_image = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    verification_token_expires_at = Column(DateTime, nullable=True)
    reset_password_token = Column(String, nullable=True)
    reset_password_token_expires_at = Column(DateTime, nullable=True)

    favorite_recipes = relationship("Recipe", secondary=user_favorites, back_populates="favorited_by")
    owned_recipes = relationship("Recipe", back_populates="recipe_owner", foreign_keys=[Recipe.owner_id])

    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")

# Refresh token model - store refresh token details
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="refresh_tokens")

