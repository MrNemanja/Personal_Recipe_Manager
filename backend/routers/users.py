from fastapi import APIRouter, Path, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User, Recipe
from schemas import CreateUser, UserResponse, RecipeResponse
from passlib.context import CryptContext

# Routes for managing users and their favorite recipes
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# GET /{id} -> get user by ID
@router.get("/{id}", response_model=UserResponse)
def get_user(id: int = Path(description="The ID of the user you want to view", gt=0), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

# POST /register -> create a new user with hashed password
@router.post("/register", response_model=UserResponse)
def register_user(user: CreateUser, db: Session = Depends(get_db)):
    if db.query(User).filter((User.username == user.username) | (User.email == user.email)).first():
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(user.password)

    new_user = User(username=user.username, password_hash=hashed_password, email=user.email, favorite_recipe_id=None)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

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
