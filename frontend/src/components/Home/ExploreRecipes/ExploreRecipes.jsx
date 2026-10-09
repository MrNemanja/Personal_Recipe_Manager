import { useState, useEffect } from "react"
import { GetAllRecipes, RegisterRecipeView } from "../../../services/RecipeService"
import { useAuth } from "../../AuthContext"
import RecipeCard from "../../RecipeCard/RecipeCard"
import RecipeModal from "../../RecipeModal/RecipeModal"
import "./ExploreRecipes.css"

function ExploreRecipes() {
    const [recipes, setRecipes] = useState([])
    const [total, setTotal] = useState(0)
    const [page, setPage] = useState(1)
    const [selectedRecipe, setSelectedRecipe] = useState(null)
    const [loading, setLoading] = useState(true)

    const { currentUser, authChecked } = useAuth()

    const LIMIT = 10
    const totalPages = Math.ceil(total / LIMIT)

     useEffect(() => {
        if (!authChecked) return

        const fetchMyRecipes = async () => {
            try {
                const offset = (page - 1) * LIMIT
    
                const response = await GetAllRecipes(LIMIT, offset)

                setRecipes(response.all_recipes)
                setTotal(response.total)
            }catch(error) {
                console.error(error)
                alert(error.response?.data?.detail || "Failed to fetch recipes")
            }finally {
                setLoading(false)
            }
        }
    
        fetchMyRecipes()
    }, [page, currentUser, authChecked])

    const handleFavorite = async (id) => {
            
        try {
            await AddFavorite(id)
    
            const offset = (page - 1) * LIMIT
            const response = await GetAllRecipes(LIMIT, offset)
    
            setRecipes(response.all_recipes)
            setTotal(response.total)
        }catch(error) {
            console.error(error)
            alert(error.response?.data?.detail || "Failed to add recipe to favorites")
        }
    }
    
    const handleRemoveFavorite = async (id) => {
    
        try {
            await RemoveFavorite(id)
    
            const offset = (page - 1) * LIMIT
            const response = await GetAllRecipes(LIMIT, offset)
    
            setRecipes(response.all_recipes)
            setTotal(response.total)
        }catch(error) {
            console.error(error)
            alert(error.response?.data?.detail || "Failed to remove recipe from favorites")
        }
    }

     const handleRecipeClick = async (recipe) => {
        setSelectedRecipe(recipe)
    
        try {
            await RegisterRecipeView(recipe.id)
        }catch(error) {
            console.error(error)
            alert(error.response?.data?.detail || "Failed to register recipe view.")
        }
    }

    return (
        <section className="explore_recipes">
            <div className="explore_recipes_content">
                <div className="explore_recipes_header">
                    <h2>Explore recipes</h2>
                    <p>Discover something new.</p>
                </div>

                {loading ? (
                    <p>Loading...</p>
                ) : (
                    <div className="explore_recipes_grid">
                        {recipes.map(recipe => (
                            <RecipeCard 
                                key={recipe.id}
                                recipe={recipe}
                                variant="home"
                                onClick={() => handleRecipeClick(recipe)}
                                onFavorite={handleFavorite}
                                onFavoriteRemove={handleRemoveFavorite}
                            />
                        ))}
                    </div>
                )}
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
}
export default ExploreRecipes