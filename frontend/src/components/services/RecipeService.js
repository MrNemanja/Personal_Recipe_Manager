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

export async function CreateRecipeRequest(recipeFormData) {
    
    const response = await api.post("/recipes/", recipeFormData)
    return response.data

}

export async function AddFavorite(recipeId) {
    
    return await api.post(`/recipes/${recipeId}/favorite`)
}

export async function RemoveFavorite(recipeId) {
    
    return await api.delete(`/recipes/${recipeId}/favorite`)
}

export async function GetMyFavorites(limit, offset) {
    
    const response = await api.get("/recipes/favorites", {
        params: {
            limit,
            offset
        }
    })
    return response.data
}

export async function UpdateRecipe(recipeId, formData) {

    const response = await api.put(`/recipes/${recipeId}`, formData)
    return response.data

}