from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Recipe: request model for creating a recipe
class Recipe(BaseModel):
    recipe_name: str = Field(..., min_length=1, description="Name of the recipe")
    recipe_ingredients: List[str] = Field(..., min_items=1, description="Ingredients of the recipe")
    preperation_time: int = Field(...,gt=0, description="Time in minutes before the ingredients are prepared")
    dish_type: str = Field(...,min_length=1, description="Type of the recipe")
    calories: int = Field(...,gt=0, description="Calories of the recipe")

# RecipeResponse: response model for returning recipe data
class RecipeResponse(BaseModel):
    id: int
    recipe_name: str
    recipe_ingredients: List[str]
    preperation_time: int
    dish_type: str
    calories: int

    class Config:
        from_attributes = True

# UpdateRecipe: request model for updating recipe fields (optional fields)
class UpdateRecipe(BaseModel):
    recipe_name: Optional[str] = Field(None, min_length=1, description="Name of the recipe")
    recipe_ingredients: Optional[list[str]] = Field(None, min_items=1, description="Ingredients of the recipe")
    preperation_time: Optional[int] = Field(None, gt=0, description="Time in minutes before the ingredients are prepared")
    dish_type: Optional[str] = Field(None, min_length=1, description="Type of the recipe")
    calories: Optional[int] = Field(None, gt=0, description="Calories of the recipe")

# CreateUser: request model for registering a user
class CreateUser(BaseModel):
    username: str = Field(...,min_length=3, description="Username")
    password: str = Field(...,min_length=6, description="Password")
    email: str = EmailStr

# UserResponse: response model for returning user info
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True