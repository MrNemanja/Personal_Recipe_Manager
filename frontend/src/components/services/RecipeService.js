import { api } from "./api"

export async function GetMyRecipes() {
    
    const response = await api.get("/recipes/me")
    return response.data
    
}