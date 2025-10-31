from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Relationship
from sqlalchemy.types import JSON
from database import Base

# Recipe model: stores recipe details
class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    recipe_name = Column(String, index=True, unique=True, nullable=False)
    recipe_ingredients = Column(JSON, nullable=False)
    preperation_time = Column(Integer, nullable=False)
    dish_type = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)

    # favorited_by establishes a many-to-one relationship with User
    favorited_by = Relationship("User", back_populates="favorite_recipe")

# User model: stores user details
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)

    # favorite_recipe_id is a foreign key to Recipe
    favorite_recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=True)

    # favorite_recipe relationship allows easy access to user's favorite recipe
    favorite_recipe = Relationship("Recipe", back_populates="favorited_by")


