from fastapi import APIRouter, HTTPException, Response, Path, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Recipe as RecipeModel
from schemas import Recipe as RecipeSchema
from schemas import UpdateRecipe, RecipeResponse
from typing import List

# Routes for managing recipes
router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)

# GET / -> list all recipes
@router.get("/", response_model=List[RecipeResponse])
async def get_recipes(db: Session = Depends(get_db)):
    recipes = db.query(RecipeModel).all()
    return recipes

# GET /{id} -> get a single recipe by ID
@router.get("/{id}", response_model=RecipeResponse)
async def get_recipe_by_id(id: int = Path(description="The ID of the recipe you want to view", gt=0), db: Session = Depends(get_db)):
    recipe = db.query(RecipeModel).filter(RecipeModel.id == id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    else:
        return recipe

# POST / -> create a new recipe
@router.post("/", response_model=RecipeResponse)
async def create_recipe(recipe: RecipeSchema, db: Session = Depends(get_db)):
    if db.query(RecipeModel).filter(RecipeModel.recipe_name == recipe.recipe_name).first():
        raise HTTPException(status_code=400, detail="Recipe already exists")

    new_recipe = RecipeModel(**recipe.dict())
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe

# PUT /{id} -> update an existing recipe
@router.put("/{id}", response_model=RecipeResponse)
async def update_recipe(id: int, updateRecipe: UpdateRecipe, db: Session = Depends(get_db)):
    recipe = db.query(RecipeModel).filter(RecipeModel.id == id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    update_data = updateRecipe.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(recipe, key, value)

    db.commit()
    db.refresh(recipe)
    return recipe

# DELETE /{id} -> delete a recipe
@router.delete("/{id}")
async def delete_recipe(id: int, db: Session = Depends(get_db)):
    recipe = db.query(RecipeModel).filter(RecipeModel.id == id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    else :
        db.delete(recipe)
        db.commit()

    return Response(status_code=204)