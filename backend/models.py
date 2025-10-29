from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.types import JSON
from database import Base

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    recipe_name = Column(String, index=True, unique=True, nullable=False)
    recipe_ingredients = Column(JSON, nullable=False)
    preperation_time = Column(Integer, nullable=False)
    dish_type = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)

class FavoriteRecipe(Base):
    __tablename__ = "favorite_recipes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)

