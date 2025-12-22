from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
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
    image_url = Column(String, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"))
    recipe_owner = relationship("User", back_populates="owned_recipes", foreign_keys=[owner_id])

    # favorited_by establishes a many-to-one relationship with User
    favorited_by = relationship("User", back_populates="favorite_recipe", foreign_keys="[User.favorite_recipe_id]")

# User model: stores user details
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    role = Column(String, nullable=False)

    # favorite_recipe_id is a foreign key to Recipe
    favorite_recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=True)

    # favorite_recipe relationship allows easy access to user's favorite recipe
    favorite_recipe = relationship("Recipe", back_populates="favorited_by", foreign_keys=[favorite_recipe_id])
    owned_recipes = relationship("Recipe", back_populates="recipe_owner", foreign_keys="[Recipe.owner_id]")


