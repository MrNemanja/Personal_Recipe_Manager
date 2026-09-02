import { useState, useEffect } from "react"
import RecipeCard from "../../../RecipeCard/RecipeCard"
import RecipeModal from "../../../RecipeModal/RecipeModal"
import { GetMyRecipes } from "../../../services/RecipeService"
import "./MyRecipes.css"

function MyRecipes() {
    const [recipes, setRecipes] = useState([])
    const [total, setTotal] = useState(0)
    const [page, setPage] = useState(1)
    const [selectedRecipe, setSelectedRecipe] = useState(null)

    const LIMIT = 6
    const totalPages = Math.ceil(total / LIMIT)

    useEffect(() => {
        const fetchMyRecipes = async () => {
            try {
                const offset = (page - 1) * LIMIT

                const response = await GetMyRecipes(LIMIT, offset)

                setRecipes(response.my_recipes)
                setTotal(response.total)
            }catch(error) {
                console.error(error)
                alert(error.response?.data?.detail || "Failed to fetch recipes")
            }
        }

        fetchMyRecipes()
    }, [page])
    
    return (
        recipes.length === 0 ? (
            <p className="no_recipes">No recipes yet.</p>
        ) : (
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
                            onClick={() => setSelectedRecipe(recipe)}
                        />
                    ))}
                </div>

                <div className="pagination">
                    <button onClick={() => setPage(page - 1)} disabled={page === 1}>
                        Previous
                    </button>

                    <span>
                        Page {page} of {totalPages}
                    </span>

                    <button onClick={() => setPage(page + 1)} disabled={page === totalPages}>
                        Next
                    </button>
                </div>

                {selectedRecipe && (
                    <RecipeModal
                        recipe={selectedRecipe}
                        onClose={() => setSelectedRecipe(null)}
                    />
                )}

            </section>
        )
    )
}
export default MyRecipes