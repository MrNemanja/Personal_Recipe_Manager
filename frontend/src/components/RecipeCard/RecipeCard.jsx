import "./RecipeCard.css"

function RecipeCard({ recipe, variant, onClick, onDelete }) {
    
    const baseURL = import.meta.env.VITE_API_URL

    const handleDelete = async (e) => {
        e.stopPropagation()

        onDelete(recipe.id)
    }

    return (
        <div className="recipe_card" onClick={onClick}>
            <img
                src={`${baseURL}/${recipe.image_url}`}
                alt={recipe.recipe_name}
                className="recipe_image"
            />

            <div className="recipe_info">
                <h3>{recipe.recipe_name}</h3>

                <div className="recipe_details">
                    <span>⏱️ {recipe.preperation_time} min</span>
                    <span>🔥 {recipe.calories} kcal</span>
                </div>

                <p className="recipe_type">
                    {recipe.dish_type}
                </p>

                <div className="recipe_actions">
                    { variant === "home" && (
                        <button className="favorite_btn">
                            ❤️ Favorite
                        </button>
                    )}

                    { variant === "my-recipes" && (
                        <>
                            <button className="favorite_btn">
                                ❤️ Favorite
                            </button>

                            <button className="edit_btn">
                                 ✏️ Edit
                            </button>

                            <button 
                                className="delete_btn"
                                onClick={handleDelete}
                            >
                                🗑️ Delete
                            </button>
                        </>
                    )}

                    { variant === "favorites" && (
                        <button className="remove_favorite_btn">
                            💔 Remove
                        </button>
                    )}
                </div>

            </div>
        </div>
    )
}
export default RecipeCard