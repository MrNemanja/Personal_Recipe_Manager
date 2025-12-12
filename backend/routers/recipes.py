import json
from fastapi import APIRouter, HTTPException, Response, Path, Query, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
from auth import get_current_user
from database import get_db
from models import Recipe as RecipeModel
from models import User
from schemas import RecipeResponse
from typing import List, Optional
from uuid import uuid4
import os

# Routes for managing recipes
router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)

UPLOAD_DIR = "images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

MAX_RECIPES = 100

# GET / -> list all recipes
@router.get("/", response_model=List[RecipeResponse])
async def get_recipes(limit: int = Query(10, gt=0, le=10, description="Max number of recipes to return"),
                      offset: int = Query(0, ge=0, description="Number of recipes to skip from the beginning"),
                      db: Session = Depends(get_db)):

    if offset >= MAX_RECIPES:
        return []

    adjusted_limit = min(limit, MAX_RECIPES - offset)

    recipes = db.query(RecipeModel).offset(offset).limit(adjusted_limit).all()
    return recipes

# GET /{id} -> get a single recipe by ID
@router.get("/{id}", response_model=RecipeResponse)
async def get_recipe_by_id(id: int = Path(description="The ID of the recipe you want to view", gt=0), db: Session = Depends(get_db)):
    recipe = db.query(RecipeModel).filter(RecipeModel.id == id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    else:
        return recipe

#GET /search/ -> get specific recipes
@router.post("/search", response_model=List[RecipeResponse])
async def get_specific_recipes(limit: int = Query(10, gt=0, le=10, description="Max number of recipes to return"),
                               offset: int = Query(0, ge=0, description="Number of recipes to skip from the beginning"),
                               recipe_ingredients: Optional[str] = None, preperation_time: Optional[int] = None,
                               dish_type: Optional[str] = None, calories: Optional[int] = None, db: Session = Depends(get_db)):

    query = db.query(RecipeModel)

    if preperation_time:
        query = query.filter(RecipeModel.preperation_time <= preperation_time)
    if dish_type:
        query = query.filter(RecipeModel.dish_type.ilike(f"%{dish_type}%"))
    if calories:
        query = query.filter(RecipeModel.calories <= calories)
    if recipe_ingredients:
        try:
            ingredients = json.loads(recipe_ingredients)
            for ingredient in ingredients:
                query = query.filter(RecipeModel.recipe_ingredients.like(f"%{ingredient}%"))
        except:
            pass

    if offset >= MAX_RECIPES:
        return []

    adjusted_limit = min(limit, MAX_RECIPES - offset)

    recipes = query.offset(offset).limit(adjusted_limit).all()
    return recipes


# POST / -> create a new recipe
@router.post("/", response_model=RecipeResponse)
async def create_recipe(recipe_name: str = Form(...), recipe_ingredients: str = Form(...),
                        preperation_time: int = Form(...), dish_type: str = Form(...),
                        calories: int = Form(...), image: UploadFile = File(),
                        current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    if db.query(RecipeModel).filter(RecipeModel.recipe_name == recipe_name).first():
        raise HTTPException(status_code=400, detail="Recipe already exists")

    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    filename = f"{uuid4()}_{image.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        contents = await image.read()
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save image: {str(e)}")

    image_url = f"/{UPLOAD_DIR}/{filename}"

    new_recipe = RecipeModel(
                            recipe_name=recipe_name, recipe_ingredients=json.loads(recipe_ingredients),
                            preperation_time=preperation_time, dish_type=dish_type, calories=calories,
                            image_url=image_url, owner_id=current_user.id
                            )

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe

# PUT /{id} -> update an existing recipe
@router.put("/{id}", response_model=RecipeResponse)
async def update_recipe(id: int, recipe_name: Optional[str] = Form(None), recipe_ingredients: Optional[str] = Form(None),
                        preperation_time: Optional[int] = Form(None), dish_type: Optional[str] = Form(None),
                        calories: Optional[int] = Form(None), image: Optional[UploadFile] = File(None),
                        current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    recipe = db.query(RecipeModel).filter(RecipeModel.id == id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if current_user.id != recipe.owner_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this recipe")

    if recipe_name:
        recipe.recipe_name = recipe_name
    if recipe_ingredients:
        recipe.recipe_ingredients = json.loads(recipe_ingredients)
    if preperation_time:
        recipe.preperation_time = preperation_time
    if dish_type:
        recipe.dish_type = dish_type
    if calories:
        recipe.calories = calories
    if image:
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        if recipe.image_url:
            old_file_path = recipe.image_url.lstrip("/")
            if os.path.exists(old_file_path):
                try:
                    os.remove(old_file_path)
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Failed to delete old image: {str(e)}")

        filename = f"{uuid4()}_{image.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        try:
            contents = await image.read()
            with open(file_path, "wb") as f:
                f.write(contents)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save new image: {str(e)}")
        recipe.image_url = f"/{UPLOAD_DIR}/{filename}"

    db.commit()
    db.refresh(recipe)
    return recipe

# DELETE /{id} -> delete a recipe
@router.delete("/{id}")
async def delete_recipe(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    recipe = db.query(RecipeModel).filter(RecipeModel.id == id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if current_user.id != recipe.owner_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this recipe")

    if recipe.image_url:
        file_path = recipe.image_url.lstrip("/")
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to delete an image: {str(e)}")

    db.delete(recipe)
    db.commit()
    return Response(status_code=204)