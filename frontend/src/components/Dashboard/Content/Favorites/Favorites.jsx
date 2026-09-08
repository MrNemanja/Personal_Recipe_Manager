import { useState, useEffect } from "react"
import RecipeCard from "../../../RecipeCard/RecipeCard"
import RecipeModal from "../../../RecipeModal/RecipeModal"
import { GetMyRecipes, DeleteRecipe, AddFavorite, RemoveFavorite, GetMyFavorites } from "../../../services/RecipeService"
import "./Favorites.css"

function Favorites({ onRecipeChange }) {
    const [favoriteRecipes, setFavoriteRecipes] = useState([])
    const [total, setTotal] = useState(0)
    const [page, setPage] = useState(1)
    const [selectedRecipe, setSelectedRecipe] = useState(null)

    const LIMIT = 6
    const totalPages = Math.ceil(total / LIMIT)

    useEffect(() => {
        const fetchMyFavorites = async () => {
            try {
                const offset = (page - 1) * LIMIT

                const response = await GetMyFavorites(LIMIT, offset)

                setFavoriteRecipes(response.favorite_recipes)
                setTotal(response.total)
            }catch(error) {
                console.error(error)
                alert(error.response?.data?.detail || "Failed to fetch favorite recipes")
            }
        }

        fetchMyFavorites()
    }, [page])

    const handleRemoveFavorite = async (id) => {

        try {
            await RemoveFavorite(id)

            onRecipeChange()

            const offset = (page - 1) * LIMIT
            const response = await GetMyFavorites(LIMIT, offset)

            setFavoriteRecipes(response.favorite_recipes)
            setTotal(response.total)
        }catch(error) {
            console.error(error)
            alert(error.response?.data?.detail || "Failed to remove recipe from favorites")
        }
    }

    return (
        favoriteRecipes.length === 0 ? (
            <p className="no_favorite_recipes">No favorite recipes yet.</p>
        ) : (
            <section className="my_favorite_recipes">
                <div className="section_header">
                    <h2>My Favorite Recipes</h2>
                    <p>Your favorite recipe collection</p>
                </div>

                <div className="recipes_grid">
                    {favoriteRecipes.map((recipe) => (
                        <RecipeCard 
                            key={recipe.id}
                            recipe={recipe}
                            variant={"favorites"}
                            onClick={() => setSelectedRecipe(recipe)}
                            onFavoriteRemove={handleRemoveFavorite}
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
export default Favorites