from fastapi import APIRouter, Path, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from database import get_db
from models import User, Recipe
from schemas import CreateUser, UserResponse, RecipeResponse, LoginUser
from passlib.context import CryptContext
from auth import create_access_token, get_current_user, get_current_user_optional
from typing import Optional

# Routes for managing users and their favorite recipes
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# GET -> get current user
@router.get("/me", response_model=Optional[UserResponse])
def get_me(current_user: Optional[User] = Depends(get_current_user_optional)):

    return current_user

# GET /{id} -> get user by ID
@router.get("/{id}", response_model=UserResponse)
def get_user(id: int = Path(description="The ID of the user you want to view", gt=0), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

# POST /register -> create a new user with hashed password
@router.post("/register")
def register_user(user: CreateUser, db: Session = Depends(get_db)):
    if db.query(User).filter((User.username == user.username) | (User.email == user.email)).first():
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(user.password)

    new_user = User(username=user.username, password_hash=hashed_password, email=user.email, role=user.role, favorite_recipe_id=None)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message" : "User registered successfully!"}

# POST /login -> Log in into your account
@router.post("/login")
def login_user(login_user: LoginUser, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_user.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not pwd_context.verify(login_user.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token({"user_id": user.id})

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        samesite="none",
        max_age=1800
    )

    return {"message": "Login successful"}

# POST /logout -> Log out and return to home page
@router.post("/logout")
def logout_user(response: Response):
    
    response.delete_cookie(key="access_token")
    return {"message": "Logged out successfully"}

# GET /{user_id}/favorite -> get user's favorite recipe
@router.get("/{user_id}/favorite", response_model=RecipeResponse)
def get_favorite_recipe(user_id: int = Path(description="The ID of the user whose favorite recipe you want to see", gt=0),
                        db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        if user.favorite_recipe_id is None:
            raise HTTPException(status_code=404, detail="User has no favorite recipe")
        else:
            return user.favorite_recipe
    else:
        raise HTTPException(status_code=404, detail="User not found")

# POST /{user_id}/favorite/{recipe_id} -> mark a recipe as favorite for user
@router.post("/{user_id}/favorite/{recipe_id}")
def mark_favorite_recipe(user_id: int = Path(description="The ID of the user you want to tag a favorite recipe to", gt=0),
                         recipe_id: int = Path(description="The ID of the recipe you want to mark as a favorite", gt=0)
                         , db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    elif not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    user.favorite_recipe_id = recipe_id
    db.commit()
    db.refresh(recipe)

    return {"message": "Recipe marked as favorite"}

# PUT /{user_id}/favorite/{new_recipe_id} -> change user's favorite recipe
@router.put("/{user_id}/favorite/{new_recipe_id}")
def update_favorite_recipe(user_id: int = Path(description="The ID of the user you want to change a favorite recipe", gt=0),
                         new_recipe_id: int = Path(description="The ID of the new recipe you want to mark as a favorite", gt=0)
                         , db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    recipe = db.query(Recipe).filter(Recipe.id == new_recipe_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    elif not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    user.favorite_recipe_id = new_recipe_id
    db.commit()
    db.refresh(recipe)

    return {"message": "New recipe marked as favorite"}

# DELETE /{user_id}/favorite -> remove user's favorite recipe
@router.delete("/{user_id}/favorite")
def delete_favorite_recipe(user_id: int = Path(description="The ID of the user whose favorite recipe you want to delete", gt=0),
                           db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.favorite_recipe_id = None
    db.commit()
    db.refresh(user)

    return {"message": "Favorite recipe deleted"}
