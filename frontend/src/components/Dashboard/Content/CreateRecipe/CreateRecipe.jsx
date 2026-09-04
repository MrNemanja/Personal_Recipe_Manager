import { useRef, useState } from "react"
import { CreateRecipeRequest } from "../../../services/RecipeService"
import "./CreateRecipe.css"

function CreateRecipe({ onRecipeChange }) {
    const [recipeFormData, setRecipeFormData] = useState({
        recipe_name : "",
        recipe_ingredients: "",
        preperation_time: "",
        dish_type: "",
        calories: "",
        image: null
    })
    const [errors, setErrors] = useState({})
    const imageInputRef = useRef(null)

    const handleInput = (e) => {
        setRecipeFormData({
            ...recipeFormData,
            [e.target.name] : e.target.files? e.target.files[0] : e.target.value
        })
    }

    const validate = () => {
        const newErrors = {}

        const ingredients = recipeFormData.recipe_ingredients
            .split(",")
            .map(ingredient => ingredient.trim())

        if (ingredients.some(ingredient => ingredient === "")) {
            newErrors.recipe_ingredients = "Please enter all ingredients correctly"
        }

        if (Number(recipeFormData.preperation_time <= 0)) {
            newErrors.preperation_time = "Preperation time must be greater than 0"
        }

        if (Number(recipeFormData.calories <= 0)) {
            newErrors.calories = "Calories must be greater than 0"
        }

        return newErrors
    }

    const handleSubmit = async (e) => {
        e.preventDefault()

        const validationErrors = validate()
        setErrors(validationErrors)

        if (Object.keys(validationErrors).length > 0) return

        const recipeDataToSend = new FormData() 

        recipeDataToSend.append("recipe_name", recipeFormData.recipe_name)
        recipeDataToSend.append("recipe_ingredients", recipeFormData.recipe_ingredients)
        recipeDataToSend.append("preperation_time", recipeFormData.preperation_time)
        recipeDataToSend.append("dish_type", recipeFormData.dish_type)
        recipeDataToSend.append("calories", recipeFormData.calories)

        if (recipeFormData.image) {
            recipeDataToSend.append("image", recipeFormData.image)
        }
        
        try { 
            const response = await CreateRecipeRequest(recipeDataToSend)

            setRecipeFormData({
                recipe_name: "",
                recipe_ingredients: "",
                preperation_time: "",
                dish_type: "",
                calories: "",
                image: null
            })
            imageInputRef.current.value = ""

            onRecipeChange()

            alert(response.message)
        
        }catch(error) {
            console.error(error)
            alert(error.response?.data?.detail || "Create recipe failed")
        }
    }
    
    return (
        <section className="create_recipe">
            <div className="section_header">
                <h2>Create Recipe</h2>
                <p>Add a new recipe to your collection</p>
            </div>

            <form onSubmit={handleSubmit}>
                <div className="form_group">
                    <label>Recipe name</label>
                    <input 
                        type="text"
                        name="recipe_name"
                        value={recipeFormData.recipe_name}
                        onChange={handleInput}
                        placeholder="Enter recipe name"
                        required
                    />
                </div>

                <div className="form_group">
                    <label>Ingredients</label>
                    <textarea
                        name="recipe_ingredients"
                        value={recipeFormData.recipe_ingredients}
                        onChange={handleInput}
                        placeholder="Enter ingredients separated by commas"
                        required
                    />
                    {errors.recipe_ingredients && (
                        <p className="error">{errors.recipe_ingredients}</p>
                    )}
                </div>

                <div className="form_group">
                    <label>Preperation Time (minutes)</label>
                    <input 
                        type="number"
                        name="preperation_time"
                        value={recipeFormData.preperation_time}
                        onChange={handleInput}
                        placeholder="e.g. 30"
                        required
                    />
                    {errors.preperation_time && (
                        <p className="error">{errors.preperation_time}</p>
                    )}
                </div>

                <div className="form_group">
                    <label>Dish Type</label>
                    <input 
                        type="text"
                        name="dish_type"
                        value={recipeFormData.dish_type}
                        onChange={handleInput}
                        placeholder="e.g. Main Course"
                        required
                    />
                </div>

                 <div className="form_group">
                    <label>Calories</label>
                    <input
                        type="number"
                        name="calories"
                        value={recipeFormData.calories}
                        onChange={handleInput}
                        placeholder="e.g. 500"
                        required
                    />
                    {errors.calories && (
                        <p className="error">{errors.calories}</p>
                    )}
                </div>

                <div className="form_group">
                    <label>Recipe Image</label>
                    <input
                        ref={imageInputRef}
                        type="file"
                        id="image"
                        name="image"
                        accept="image/*"
                        onChange={handleInput}
                    />
                </div>

                <button type="submit">
                    Create Recipe
                </button>
            </form>
        </section>
    )
}
export default CreateRecipe