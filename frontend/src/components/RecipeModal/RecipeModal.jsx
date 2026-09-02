import "./RecipeModal.css"

function RecipeModal({ recipe, onClose }) {
    const baseURL = import.meta.env.VITE_API_URL

    return (
        <div className="recipe_modal_overlay" onClick={onClose}>
            <div className="recipe_modal" onClick={(e) => e.stopPropagation()}>
                <button className="modal_close_btn" onClick={onClose}>
                    ✕
                </button>

                <img
                    src={`${baseURL}/${recipe.image_url}`}
                    alt={recipe.recipe_name}
                    className="modal_recipe_image"
                />

                <div className="modal_recipe_info">
                    <h2>{recipe.recipe_name}</h2>

                    <div className="modal_recipe_details">
                        <span>⏱️ {recipe.preperation_time} min</span>
                        <span>🔥 {recipe.calories} kcal</span>
                    </div>

                    <p className="modal_recipe_type">
                        {recipe.dish_type}
                    </p>

                    <div className="modal_section">
                        <h3>Ingredients</h3>

                         <ul>
                            {recipe.recipe_ingredients.map((ingredient, index) => (
                                <li key={index}>{ingredient}</li>
                            ))}
                        </ul>
                    </div>
                </div>

            </div>
        </div>
    )
}
export default RecipeModal