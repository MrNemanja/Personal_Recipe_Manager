import { useState, useEffect } from "react"
import { GetRecipeOfTheDay } from "../../../services/RecipeService"
import "./RecipeOfTheDay.css"

function RecipeOfTheDay() {
    const baseURL = import.meta.env.VITE_API_URL
    
    const [recipe, setRecipe] = useState(null)
    const [noRecipes, setNoRecipes] = useState(false)
    const [loading, setLoading] = useState(true)
    
    useEffect(() => {
        const fetchRecipeOfTheDay = async () => {
            try {
                const response = await GetRecipeOfTheDay()
                setRecipe(response)
            }catch(error) {
                if (error.response?.status === 404) {
                    setNoRecipes(true)
                } else {
                    console.error(error)
                    alert(error.response?.data?.detail || "Failed to fetch recipe of the day.")
                }
            }finally {
                setLoading(false)
            }
        }

        fetchRecipeOfTheDay()
    }, [])
    
    return (
        <section className="recipe_of_the_day">
            <div className="recipe_of_the_day_content">
                
                <div className="recipe_of_the_day_header">
                    <h2>Recipe of the Day</h2>
                    <p>A recipe worth trying today.</p>
                </div>

                {loading ? (
                    <p>Loading...</p>
                ) : noRecipes ? (
                    <p>No recipes yet.</p>
                ) : (
                    <div className="recipe_of_the_day_card">
                    <div className="recipe_of_the_day_image">
                        <img 
                            src={`${baseURL}/${recipe.image_url}`}
                            alt={recipe.recipe_name}
                        />
                    </div>

                    <div className="recipe_of_the_day_info">
                        <h3>{recipe.recipe_name}</h3>

                        <div className="recipe_of_the_day_meta">
                            <span>⏱ {recipe.preperation_time} min</span>
                            <span>🍽 {recipe.dish_type}</span>

                            <p>
                                🔥 {recipe.calories}
                            </p>

                            <button>
                                View Recipe
                            </button>
                        </div>
                    </div>
                    </div>
                )}
            </div>
        </section>
    )
}
export default RecipeOfTheDay