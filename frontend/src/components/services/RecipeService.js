import { api } from "./api"

export async function GetMyRecipes(limit, offset) {
    
    const response = await api.get("/recipes/me", {
        params: {
            limit,
            offset
        }
    })
    return response.data
    
}

export async function GetMyStats() {
    
    const response = await api.get("/recipes/me/stats")
    return response.data

}

export async function DeleteRecipe(recipeId) {
    return await api.delete(`/recipes/${recipeId}`)
}