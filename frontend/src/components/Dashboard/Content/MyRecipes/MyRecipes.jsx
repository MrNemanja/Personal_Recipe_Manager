import { useState, useEffect } from "react"
import RecipeCard from "../../../RecipeCard/RecipeCard"
import { GetMyRecipes } from "../../../services/RecipeService"
import "./MyRecipes.css"

function MyRecipes() {
    const [recipes, setRecipes] = useState([])

    useEffect(() => {
        const fetchMyRecipes = async () => {
            try {
                const response = await GetMyRecipes()
                setRecipes(response)
            }catch(error) {
                console.error(error)
                alert(error.response?.data?.detail || "Failed to fetch recipes")
            }
        }

        fetchMyRecipes()
    }, [])
    
    return (
        <section className="my_recipes">
            <div className="section_header">
                <h2>My Recipes</h2>
                <p>Your personal recipe collection</p>
            </div>

            <div className="recipes_grid">
                {recipes.map((recipe) => (
                    <RecipeCard 
                        key={recipe.id}
                        recipe={recipe}
                        variant={"my-recipes"}
                    />
                ))}
            </div>
        </section>
    )
}
export default MyRecipes