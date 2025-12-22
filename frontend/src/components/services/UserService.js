import { api } from "./api";

export async function getCurrentUser() {
    const response = await api.get("/users/me")
    return response.data
}


export async function RegisterUser(formData) {

    const response = await api.post("/users/register", formData)
    return response.data

}
export async function LoginUser(formData) {
    
    const response = await api.post("/users/login", formData)
    return response.data
}

export async function LogoutUser() {
    
    const response = await api.post("/users/logout")
    return response.data
}
