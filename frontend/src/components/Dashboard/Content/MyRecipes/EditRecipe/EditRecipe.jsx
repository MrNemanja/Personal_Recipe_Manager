import { useState } from "react"
import { UpdateRecipe } from "../../../../services/RecipeService"
import "./EditRecipe.css"

function EditRecipe({ recipe, onClose, onRecipeUpdated }) {
    const [editRecipeFormData, setEditRecipeFormData] = useState({
        recipe_name: recipe.recipe_name,
        recipe_ingredients: recipe.recipe_ingredients.join(", "),
        preperation_time: recipe.preperation_time,
        dish_type: recipe.dish_type,
        calories: recipe.calories,
        image: null
    })
    const [errors, setErrors] = useState({})
    const [loading, setLoading] = useState(false)
    
    const handleInput = (e) => {
        setEditRecipeFormData({
            ...editRecipeFormData,
            [e.target.name] : e.target.files? e.target.files[0] : e.target.value
        })
    }

    const validate = () => {
        const newErrors = {}

        const ingredients = editRecipeFormData.recipe_ingredients
            .split(",")
            .map(ingredient => ingredient.trim())

        if (ingredients.some(ingredient => ingredient === "")) {
            newErrors.recipe_ingredients = "Please enter all ingredients correctly"
        }

        return newErrors
    }

    const handleSubmit = async (e) => {
        e.preventDefault()

        const validationErrors = validate()
        setErrors(validationErrors)

        if (Object.keys(validationErrors).length > 0) return

         const recipeDataToSend = new FormData() 

        recipeDataToSend.append("recipe_name", editRecipeFormData.recipe_name)
        recipeDataToSend.append("recipe_ingredients", editRecipeFormData.recipe_ingredients)
        recipeDataToSend.append("preperation_time", editRecipeFormData.preperation_time)
        recipeDataToSend.append("dish_type", editRecipeFormData.dish_type)
        recipeDataToSend.append("calories", editRecipeFormData.calories)

        if (editRecipeFormData.image) {
            recipeDataToSend.append("image", editRecipeFormData.image)
        }

        try {
            setLoading(true)

            const updatedRecipe = await UpdateRecipe(recipe.id, recipeDataToSend)

            console.log("UPDATED RECIPE:", updatedRecipe)

            onRecipeUpdated(updatedRecipe)
            onClose()

        } catch (error) {
            console.error(error)
            alert(error.response?.data?.detail || "Update recipe failed")
        } finally {
            setLoading(false)
        }
    }

    return (
         <div className="edit_recipe_overlay">

            <div className="edit_recipe_modal">

                <button
                    className="close_edit_recipe"
                    onClick={onClose}
                    type="button"
                >
                    ✕
                </button>

                <div className="edit_recipe_header">
                    <h2>Edit Recipe</h2>
                    <p>Update your recipe information</p>
                </div>

                <form
                    className="edit_recipe_form"
                    onSubmit={handleSubmit}
                >

                    <div className="form_group">
                        <label htmlFor="recipe_name">
                            Recipe Name
                        </label>

                        <input
                            id="recipe_name"
                            name="recipe_name"
                            type="text"
                            value={editRecipeFormData.recipe_name}
                            onChange={handleInput}
                            required
                        />
                    </div>

                    <div className="form_group">
                        <label htmlFor="recipe_ingredients">
                            Ingredients
                        </label>

                        <textarea
                            id="recipe_ingredients"
                            name="recipe_ingredients"
                            value={editRecipeFormData.recipe_ingredients}
                            onChange={handleInput}
                            required
                        />
                        {errors.recipe_ingredients && (
                            <p className="edit_recipe_error">{errors.recipe_ingredients}</p>
                        )}
                    </div>

                    <div className="form_row">

                        <div className="form_group">
                            <label htmlFor="preperation_time">
                                Preparation Time (min)
                            </label>

                            <input
                                id="preperation_time"
                                name="preperation_time"
                                type="number"
                                min="1"
                                value={editRecipeFormData.preperation_time}
                                onChange={handleInput}
                                required
                            />
                        </div>

                        <div className="form_group">
                            <label htmlFor="calories">
                                Calories
                            </label>

                            <input
                                id="calories"
                                name="calories"
                                type="number"
                                min="1"
                                value={editRecipeFormData.calories}
                                onChange={handleInput}
                                required
                            />
                        </div>

                    </div>

                    <div className="form_group">
                        <label htmlFor="dish_type">
                            Dish Type
                        </label>

                        <input
                            id="dish_type"
                            name="dish_type"
                            type="text"
                            value={editRecipeFormData.dish_type}
                            onChange={handleInput}
                            required
                        />
                    </div>

                    <div className="form_group">
                        <label htmlFor="image">
                            New Image (optional)
                        </label>

                        <input
                            id="image"
                            name="image"
                            type="file"
                            accept="image/*"
                            onChange={handleInput}
                        />

                        {editRecipeFormData.image && (
                            <p className="selected_image">
                                Selected: {editRecipeFormData.image.name}
                            </p>
                        )}
                    </div>

                    <div className="edit_recipe_actions">

                        <button
                            type="button"
                            className="cancel_edit_btn"
                            onClick={onClose}
                            disabled={loading}
                        >
                            Cancel
                        </button>

                        <button
                            type="submit"
                            className="update_recipe_btn"
                            disabled={loading}
                        >
                            {loading ? "Updating..." : "Update Recipe"}
                        </button>

                    </div>

                </form>

            </div>

        </div>
    )
}
export default EditRecipe