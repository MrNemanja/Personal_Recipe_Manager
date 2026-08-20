import json
from datetime import date

from fastapi import Form
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Recipe: request model for creating a recipe
class CreateRecipe(BaseModel):
    recipe_name: str = Field(..., min_length=1, description="Name of the recipe")
    recipe_ingredients: List[str] = Field(..., min_items=1, description="Ingredients of the recipe")
    preperation_time: int = Field(...,gt=0, description="Time in minutes before the ingredients are prepared")
    dish_type: str = Field(...,min_length=1, description="Type of the recipe")
    calories: int = Field(...,gt=0, description="Calories of the recipe")

    @classmethod
    def as_form(
            cls, recipe_name: str = Form(), recipe_ingredients: str = Form(), preperation_time: int = Form(),
            dish_type: str = Form(), calories: int = Form()):

        return cls(
            recipe_name=recipe_name,
            recipe_ingredients=recipe_ingredients.split(","),
            preperation_time=preperation_time,
            dish_type=dish_type,
            calories=calories
        )

# UpdateRecipe: request model for updating recipe fields (optional fields)
class UpdateRecipe(BaseModel):
    recipe_name: Optional[str] = Field(None, min_length=1, description="Name of the recipe")
    recipe_ingredients: Optional[list[str]] = Field(None, min_items=1, description="Ingredients of the recipe")
    preperation_time: Optional[int] = Field(None, gt=0, description="Time in minutes before the ingredients are prepared")
    dish_type: Optional[str] = Field(None, min_length=1, description="Type of the recipe")
    calories: Optional[int] = Field(None, gt=0, description="Calories of the recipe")

# RecipeResponse: response model for returning recipe data
class RecipeResponse(BaseModel):
    id: int
    recipe_name: str
    recipe_ingredients: List[str]
    preperation_time: int
    dish_type: str
    calories: int
    image_url : Optional[str] = None

    class Config:
        from_attributes = True

class CreateUser(BaseModel):
    username: str = Field(..., min_length=3, description="Username")
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., min_length=6, description="Password")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name of the user")
    phone : Optional[str] = Field(None, max_length=50, description="Phone number of the user")
    city: Optional[str] = Field(None, max_length=50, description="City of the user")
    country: Optional[str] = Field(None, max_length=50, description="Country of the user")
    dob: Optional[date] = Field(None, description="Date of birth of the user")

    @classmethod
    def as_form(cls, username: str = Form(), email: EmailStr = Form(), password: str = Form(),
                full_name: str = Form(None), phone: str = Form(None), city: str = Form(None),
                country: str = Form(None), dob: date = Form(None)):

        return cls(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            phone=phone,
            city=city,
            country=country,
            dob=dob
        )

class VerifyEmail(BaseModel):
    token: str

class ResendEmail(BaseModel):
    email: EmailStr

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(...,min_length=6, description="New Password")

class LoginUser(BaseModel):
    username: str
    password: str

# UserResponse: response model for returning user info
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    profile_image: Optional[str]

    class Config:
        from_attributes = True

# UserProfileResponse: response model for returning user profile info
class UserProfileResponse(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str]
    phone: Optional[str]
    city: Optional[str]
    country: Optional[str]
    dob: Optional[date]
    profile_image: Optional[str]

    class Config:
        from_attributes = True

class UpdateProfile(BaseModel):
    full_name : Optional[str] = Field(None, max_length=100, description="Full name of the user")
    phone : Optional[str] = Field(None, max_length=50, description="Phone number of the user")
    city: Optional[str] = Field(None, max_length=50, description="City of the user")
    country: Optional[str] = Field(None, max_length=50, description="Country of the user")
    dob: Optional[date] = Field(None, description="Date of birth of the user")

    @classmethod
    def as_form(cls, full_name: str = Form(None), phone: str = Form(None), city: str = Form(None),
                country: str = Form(None), dob: date = Form(None)):

        return cls(
            full_name=full_name,
            phone=phone,
            city=city,
            country=country,
            dob=dob
        )