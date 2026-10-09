import json
from fastapi import APIRouter, HTTPException, Response, Path, Query, Depends, File, UploadFile, Header
from sqlalchemy.orm import Session
from auth import get_current_user, get_current_user_optional
from datetime import datetime, timedelta
from database import get_db
from models import Recipe as RecipeModel, user_favorites, RecipeView
from models import User
from schemas import RecipeResponse, CreateRecipe, UserStatsResponse, MyRecipesResponse, MyFavoriteRecipesResponse, \
    UpdateRecipe, AllRecipesResponse
from typing import List, Optional
from services.file_service import save_recipe_image, delete_image
import os

# Routes for managing recipes
router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)

UPLOAD_DIR = "recipe_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# GET / -> list all recipes
@router.get("/", response_model=AllRecipesResponse)
async def get_all_recipes(limit: int = Query(10, gt=0, le=10, description="Max number of recipes to return"),
                      offset: int = Query(0, ge=0, description="Number of recipes to skip from the beginning"),
                      current_user: Optional[User] = Depends(get_current_user_optional),
                      db: Session = Depends(get_db)):

    query = db.query(RecipeModel).order_by(RecipeModel.id.desc())

    total = query.count()

    all_recipes = query.offset(offset).limit(limit).all()

    all_recipes = [
        {
            "id": recipe.id,
            "recipe_name": recipe.recipe_name,
            "recipe_ingredients": recipe.recipe_ingredients,
            "preperation_time": recipe.preperation_time,
            "dish_type": recipe.dish_type,
            "calories": recipe.calories,
            "image_url": recipe.image_url,
            "is_favorite": current_user is not None and recipe in current_user.favorite_recipes
        }
        for recipe in all_recipes
    ]

    return {
        "all_recipes": all_recipes,
        "total": total,
    }

@router.get("/me", response_model=MyRecipesResponse)
async def get_my_recipes(
        limit: int = Query(6, gt=0, le=6, description="Max number of recipes to return"),
        offset: int = Query(0, ge=0, description="Number of recipes to skip from the beginning"),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    query = db.query(RecipeModel).filter(RecipeModel.owner_id == current_user.id).order_by(RecipeModel.id.desc())

    total = query.count()

    my_recipes = query.offset(offset).limit(limit).all()

    my_recipes = [
        {
            "id": recipe.id,
            "recipe_name": recipe.recipe_name,
            "recipe_ingredients": recipe.recipe_ingredients,
            "preperation_time": recipe.preperation_time,
            "dish_type": recipe.dish_type,
            "calories": recipe.calories,
            "image_url": recipe.image_url,
            "is_favorite": recipe in current_user.favorite_recipes
        }
        for recipe in my_recipes
    ]

    return {
        "my_recipes": my_recipes,
        "total": total,
    }

@router.get("/me/stats", response_model=UserStatsResponse)
async def get_my_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    recipe_count = (
        db.query(RecipeModel)
        .filter(RecipeModel.owner_id == current_user.id)
        .count()
    )

    favorite_count = (
        db.query(user_favorites)
        .filter(user_favorites.c.user_id == current_user.id)
        .count()
    )

    return {
        "recipe_count": recipe_count,
        "favorite_count": favorite_count,
    }

@router.get("/favorites", response_model=MyFavoriteRecipesResponse)
def get_user_favorites(current_user: User = Depends(get_current_user),
                       db: Session = Depends(get_db),
                       limit: int = Query(6, gt=0, le=6, description="Max number of recipes to return"),
                       offset: int = Query(0, ge=0, description="Number of recipes to skip from the beginning")
):

    query = (
        db.query(RecipeModel)
        .join(
            user_favorites,
            RecipeModel.id == user_favorites.c.recipe_id,
        )
        .filter(
            user_favorites.c.user_id == current_user.id
        )
        .order_by(RecipeModel.id.desc())
    )

    total = query.count()

    favorite_recipes = query.offset(offset).limit(limit).all()

    favorite_recipes = [
        {
            "id": favorite_recipe.id,
            "recipe_name": favorite_recipe.recipe_name,
            "recipe_ingredients": favorite_recipe.recipe_ingredients,
            "preperation_time": favorite_recipe.preperation_time,
            "dish_type": favorite_recipe.dish_type,
            "calories": favorite_recipe.calories,
            "image_url": favorite_recipe.image_url,
            "is_favorite": True
        }
        for favorite_recipe in favorite_recipes
    ]

    return {
        "favorite_recipes": favorite_recipes,
        "total": total
    }

# GET /rotd -> get recipe of the day
@router.get("/rotd", response_model=RecipeResponse)
async def get_recipe_of_the_day(current_user: User = Depends(get_current_user_optional),db: Session = Depends(get_db)):
    recipes = db.query(RecipeModel).all()

    if not recipes:
        raise HTTPException(status_code=404, detail="No recipes found")

    scores = {}

    for recipe in recipes:
        scores[recipe.id] = len(recipe.favorited_by) * 5 + len(recipe.views)

    max_id = max(scores, key=scores.get)

    for recipe in recipes:
        if recipe.id == max_id:
            return {
                "id": recipe.id,
                "recipe_name": recipe.recipe_name,
                "recipe_ingredients": recipe.recipe_ingredients,
                "preperation_time": recipe.preperation_time,
                "dish_type": recipe.dish_type,
                "calories": recipe.calories,
                "image_url": recipe.image_url,
                "is_favorite": current_user is not None and recipe in current_user.favorite_recipes
            }

# GET /{id} -> get a single recipe by ID
@router.get("/{id}", response_model=RecipeResponse)
async def get_recipe_by_id(id: int = Path(description="The ID of the recipe you want to view", gt=0), db: Session = Depends(get_db)):
    recipe = db.query(RecipeModel).filter(RecipeModel.id == id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    else:
        return recipe

# POST /{id}/view -> Register recipe view
@router.post("/{id}/view")
async def register_recipe_view(id: int = Path(description="The ID of the recipe you want to register view"),
                               visitor_id: str | None = Header(default=None, alias="X-Visitor-ID"),
                               db: Session = Depends(get_db),
                               current_user: User = Depends(get_current_user_optional)):

    recipe = db.query(RecipeModel).filter(RecipeModel.id == id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)

    if current_user:
        existing_view = (
                db.query(RecipeView)
                .filter(
                    RecipeView.recipe_id == id,
                    RecipeView.user_id == current_user.id,
                    RecipeView.viewed_at >= twenty_four_hours_ago
                ).first()
        )
    else:
        if not visitor_id:
            raise HTTPException(status_code=400, detail="Visitor ID required for unauthenticated users")

        existing_view = (
            db.query(RecipeView)
            .filter(
                RecipeView.recipe_id == id,
                RecipeView.visitor_id == visitor_id,
                RecipeView.viewed_at >= twenty_four_hours_ago
            ).first()
        )

    if existing_view:
        return Response(status_code=204)

    recipe_view = RecipeView(
        recipe_id=id,
        user_id=current_user.id if current_user else None,
        visitor_id=visitor_id,
    )

    db.add(recipe_view)
    db.commit()

    return Response(status_code=204)

# GET /search/ -> get specific recipes
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

    recipes = query.offset(offset).limit(limit).all()
    return recipes

# POST / -> create a new recipe
@router.post("/")
async def create_recipe(recipe_data: CreateRecipe = Depends(CreateRecipe.as_form) , image: UploadFile = File(None),
                        current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    if db.query(RecipeModel).filter(RecipeModel.recipe_name == recipe_data.recipe_name).first():
        raise HTTPException(status_code=400, detail="Recipe already exists")

    recipe_image_path = save_recipe_image(image) if image else None

    new_recipe = RecipeModel(
                            recipe_name=recipe_data.recipe_name, recipe_ingredients=recipe_data.recipe_ingredients,
                            preperation_time=recipe_data.preperation_time, dish_type=recipe_data.dish_type,
                            calories=recipe_data.calories, image_url=recipe_image_path, owner_id=current_user.id
                            )

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    return {"message" : "Recipe created successfully"}

# PUT /{id} -> update an existing recipe
@router.put("/{id}", response_model=RecipeResponse)
async def update_recipe(id: int,
                        recipe_data: UpdateRecipe = Depends(UpdateRecipe.as_form),
                        image: Optional[UploadFile] = File(None),
                        current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    recipe = db.query(RecipeModel).filter(RecipeModel.id == id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if current_user.id != recipe.owner_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this recipe")

    if recipe_data.recipe_name is not None:
        recipe.recipe_name = recipe_data.recipe_name
    if recipe_data.recipe_ingredients is not None:
        recipe.recipe_ingredients = recipe_data.recipe_ingredients
    if recipe_data.preperation_time is not None:
        recipe.preperation_time = recipe_data.preperation_time
    if recipe_data.dish_type is not None:
        recipe.dish_type = recipe_data.dish_type
    if recipe_data.calories is not None:
        recipe.calories = recipe_data.calories

    if image:
      old_image = recipe.image_url
      new_image = save_recipe_image(image)
      recipe.image_url = new_image
      delete_image(old_image)

    db.commit()
    db.refresh(recipe)

    return {
        "id": recipe.id,
        "recipe_name": recipe.recipe_name,
        "recipe_ingredients": recipe.recipe_ingredients,
        "preperation_time": recipe.preperation_time,
        "dish_type": recipe.dish_type,
        "calories": recipe.calories,
        "image_url": recipe.image_url,
        "is_favorite": recipe in current_user.favorite_recipes
    }

# DELETE /{id} -> delete a recipe
@router.delete("/{id}")
async def delete_recipe(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    recipe = db.query(RecipeModel).filter(RecipeModel.id == id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if current_user.id != recipe.owner_id:
        raise HTTPException(status_code=403, detail="You are not the owner of this recipe")

    if recipe.image_url:
        delete_image(recipe.image_url)

    db.delete(recipe)
    db.commit()
    return Response(status_code=204)

@router.post("/{id}/favorite")
def add_favorite(
        id: int = Path(description="The ID of the recipe you want to add to favorites", gt=0),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    recipe = db.query(RecipeModel).filter(RecipeModel.id == id).first()

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if recipe in current_user.favorite_recipes:
        raise HTTPException(status_code=400, detail="Recipe is already in favorites")

    current_user.favorite_recipes.append(recipe)

    db.commit()

    return Response(status_code=201)

@router.delete("/{id}/favorite")
def remove_favorite(
        id: int = Path(description="The ID of the recipe you want to remove from favorites", gt=0),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):
    result = db.execute(
        user_favorites.delete().where(
            user_favorites.c.recipe_id == id,
            user_favorites.c.user_id == current_user.id,
        )
    )

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Favorite recipe not found")

    db.commit()

    return Response(status_code=204)