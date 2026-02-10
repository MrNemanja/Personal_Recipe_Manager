import { api } from "./api";

export async function getCurrentUser() {
    
    const response = await api.get("/users/me")
    return response.data
}

export async function RegisterUser(formData) {

    const response = await api.post("/users/register", formData)
    return response.data
}

export async function VeifyUserEmail(token) {
    
    const response = await api.post("/users/verify-email", token)
    return response.data
}

export async function ResendVerificationEmail(email) {

    const response = await api.post("/users/resend-verification", email)
    return response.data
}

export async function LoginUser(formData) {
    
    const response = await api.post("/users/login", formData)
    return response.data
}

export async function RefreshAccessToken() {
    
    await api.post("/users/refresh")
}

export async function requestPasswordReset(email) {
    
    const response = await api.post("/users/forgot-password", email)
    return response.data
}

export async function resetPassword(data) {
    
    const response = await api.post("/users/reset-password", data)
    return response.data
}

export async function LogoutUser() {
    
    const response = await api.post("/users/logout")
    return response.data
}
