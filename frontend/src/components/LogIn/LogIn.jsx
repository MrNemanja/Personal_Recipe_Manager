import './LogIn.css'
import { useState } from 'react'

function LogIn() {
     
    const [formData, setFormData] = useState({
        username: "",
        password: ""
    })
    const [errors, setErrors] = useState({})

    const handleInput = (e) => {
        setFormData({
            ...formData,
            [e.target.name] : e.target.value
        })
    }

    return(
        <div className="login-card">
            <h2>Welcome Back</h2>
            <p className="subtitle">Log in to manage your recipes</p>

            <form className="login-form">
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