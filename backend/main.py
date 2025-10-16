from fastapi import FastAPI, HTTPException, Path
from typing import Optional
from pydantic import BaseModel, Field

#Start-up for FastAPI
app = FastAPI()

#Test-data
dummy_list = {
    1: {
        "recipe_name" : "Karbonara",
        "recipe_ingredients" : ["Pecorino", "Bacon", "White Onion", "Eggs", "Spaghetti"],
        "preperation_time" : 40,
        "dish_type" : "savory",
        "calories" : 500
    },
    2: {
        "recipe_name" : "Pizza Capricciosa",
        "recipe_ingredients" : ["Cheese", "Ham", "Mushsrooms", "Pelata", "Oregano"],
        "preperation_time" : 20,
        "dish_type" : "savory",
        "calories" : 900
    },
    3: {
        "recipe_name" : "Cheese Cake",
        "recipe_ingredients" : ["Strawberries", "Plasma Biscuit", "Sour Cream", "Powdered Sugar"],
        "preperation_time" : 60,
        "dish_type" : "sweet",
        "calories" : 1500
    }
}

#In this format our backend need to get data from our frontend. This refers to POST method
class Recipe(BaseModel):
    recipe_name: str = Field(..., min_length=1, description="Name of the recipe")
    recipe_ingredients: list[str] = Field(..., min_items=1, description="Ingredients of the recipe")
    preperation_time: int = Field(...,gt=0, description="Time in minutes before the ingredients are prepared")
    dish_type: str = Field(...,min_length=1, description="Type of the recipe")
    calories: int = Field(...,gt=0, description="Calories of the recipe")

#In this format our backend need to get data from our frontend. This refers to PUT method
class UpdateRecipe(BaseModel):
    recipe_name: Optional[str] = Field(None, min_length=1, description="Name of the recipe")
    recipe_ingredients: Optional[list[str]] = Field(None, min_items=1, description="Ingredients of the recipe")
    preperation_time: Optional[int] = Field(None, gt=0, description="Time in minutes before the ingredients are prepared")
    dish_type: Optional[str] = Field(None, min_length=1, description="Type of the recipe")
    calories: Optional[int] = Field(None, gt=0, description="Calories of the recipe")

#Get recipe by recipe id
@app.get("/recipes/{id}")
async def recipes(*, id: int = Path(description="The ID of the recipe you want to view", gt=0), limit: Optional[int] = None, search: Optional[str] = None):
    if id in dummy_list:
        if limit is None and search is None:
            return {"recipe" : dummy_list[id]}
        elif limit is not None and search is not None:
            if len(dummy_list[id]["recipe_ingredients"]) <= limit and any(ingredient.lower() == search.lower() for ingredient in dummy_list[id]["recipe_ingredients"]):
                return {"recipe" : dummy_list[id]}
            else:
                raise HTTPException(status_code=404, detail="Recipe not found")
        elif limit is None and search is not None:
            if any(ingredient.lower() == search.lower() for ingredient in dummy_list[id]["recipe_ingredients"]):
                return {"recipe" : dummy_list[id]}
            else :
                raise HTTPException(status_code=404, detail="Recipe not found")
        else:
            if len(dummy_list[id]["recipe_ingredients"]) <= limit:
                return {"recipe" : dummy_list[id]}
            else:
                raise HTTPException(status_code=404, detail="Recipe not found")

    else:
        raise HTTPException(status_code=404, detail="Recipe not found")

#Create new recipe
@app.post("/recipes")
async def create_recipe(recipe: Recipe):

    new_id = max(dummy_list.keys(), default=0) + 1
    dummy_list[new_id] = recipe.model_dump()

    return {"id" : new_id, "message" : "Recipe created successfully"}

#Update existing recipe
@app.put("/recipes/{id}")
async def update_recipe(id: int, recipe: UpdateRecipe):
    if id not in dummy_list:
        raise HTTPException(status_code=404, detail="Recipe not found")
    else:
        if recipe.recipe_name != None:
            dummy_list[id]["recipe_name"] = recipe.recipe_name
        if recipe.recipe_ingredients != None:
            dummy_list[id]["recipe_ingredients"] = recipe.recipe_ingredients
        if recipe.preperation_time != None:
            dummy_list[id]["preperation_time"] = recipe.preperation_time
        if recipe.dish_type != None:
            dummy_list[id]["dish_type"] = recipe.dish_type
        if recipe.calories != None:
            dummy_list[id]["calories"] = recipe.calories

    return {"id" : id, "message" : "Recipe updated successfully"}

#Delete existing recipe
@app.delete("/recipes/{id}")
async def delete_recipe(id: int):
    if id not in dummy_list:
        raise HTTPException(status_code=404, detail="Recipe not found")
    else:
        del dummy_list[id]

    return {"id" : id, "message" : "Recipe deleted successfully"}