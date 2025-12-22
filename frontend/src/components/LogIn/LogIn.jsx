import './LogIn.css'
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { LoginUser, getCurrentUser } from '../services/UserService'

function LogIn({setCurrentUser}) {
     
    const [formData, setFormData] = useState({
        username: "",
        password: ""
    })
    const navigate = useNavigate()

    
    const handleInput = (e) => {
        setFormData({
            ...formData,
            [e.target.name] : e.target.value
        })
    }

    const handleSubmit = async(e) => {
        
        e.preventDefault()
        try{

            await LoginUser(formData)
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

            <p className="register-text">
                Don't have an account? <a href="/register">Register</a>
            </p>
        </div>
    )
}
export default LogIn