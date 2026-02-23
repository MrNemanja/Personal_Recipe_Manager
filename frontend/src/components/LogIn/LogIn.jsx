import './LogIn.css'
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { LoginUser, getCurrentUser } from '../services/UserService'
import { useAuth } from '../AuthContext'
import MfaModal from '../MFA/MfaModal'

function LogIn() {
     
    const [formData, setFormData] = useState({
        username: "",
        password: ""
    })
    const [showMfa, setShowMfa] = useState(false)
    const [mfaToken, setMfaToken] = useState(null)
    const navigate = useNavigate()
    const { setCurrentUser } = useAuth()
    
    const handleInput = (e) => {
        setFormData({
            ...formData,
            [e.target.name] : e.target.value
        })
    }

    const handleSubmit = async(e) => {
        
        e.preventDefault()
        try{

            const response = await LoginUser(formData)

            if(response.mfa_required) {
                setMfaToken(response.mfa_token);
                setShowMfa(true);
                return;
            }

            const user = await getCurrentUser()
            setCurrentUser(user)
            if (user.role === "admin") navigate("/adminDashboard")
            else navigate("/dashboard")


        }catch(error) {
            console.error(error)
            alert(error.response?.data?.detail || "LogIn failed")
        }
    }


    return(
        <div className="login-card">
            <h2>Welcome Back</h2>
            <p className="subtitle">Log in to manage your recipes</p>

            <form className="login-form" onSubmit={handleSubmit}>
                <label>Username</label>
                <input type="text" placeholder="Enter your username" value={formData.username} 
                name="username" onChange={handleInput} required/>

                <label>Password</label>
                <input type="password" placeholder="Enter your password" value={formData.password}
                name="password" onChange={handleInput} required/>

                <button type="submit" className="login-btn">Log In</button>
            </form>
            <p className="redirect">
                <a href="/forgot-password">Forgot your password?</a>
            </p>
            <p className="register-text">
                Don't have an account? <a href="/register">Register</a>
            </p>

            {showMfa && <MfaModal mfaToken = {mfaToken} mode='login' onSuccess={
                async () => {
                     const user = await getCurrentUser()
                     setCurrentUser(user)
                     if (user.role === "admin") navigate("/adminDashboard")
                     else navigate("/dashboard")
                }} />}
        </div>
    )
}
export default LogIn