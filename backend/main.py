from fastapi import FastAPI, HTTPException, Path
from typing import Optional
app = FastAPI()

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

