import { useState, useEffect } from "react"
import { GetMyStats } from "../../../services/RecipeService"
import "./Stats.css"

function Stats({ refresh }) {
    const [myRecipeCount, setMyRecipeCount] = useState(0)
    const [myFavoriteCount, setMyFavoriteCount] = useState(0)

    useEffect(() => {
        const fetchMyStats = async () => {
            try {
                const response = await GetMyStats()
                setMyRecipeCount(response.recipe_count)
                setMyFavoriteCount(response.favorite_count)
            }catch(error) {
                console.error(error)
                alert(error.response?.data?.detail || "Failed to fetch recipe count.")
            }
        }
        fetchMyStats()
    }, [refresh])

    return (
        <div className="stats">
            <div className="stat_card">
                <span>🍳</span>
                <div>
                    <strong>{myRecipeCount}</strong>
                    <p>My Recipes</p>
                </div>
            </div>
            <div className="stat_card">
                <span>❤️</span>
                <div>
                    <strong>{myFavoriteCount}</strong>
                    <p>Favorites</p>
                </div>
            </div>
        </div>
    )
}
export default Stats