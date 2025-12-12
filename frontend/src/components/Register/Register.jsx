import './Register.css'
import {useState} from 'react'

function Register() {
    
    const [formData, setFormData] = useState({
        username: "",
        email: "",
        password: "",
        confirmPassword: ""
    })
    const [errors, setErrors] = useState({})
    

    const handleInput = (e) => {
        setFormData({
            ...formData,
            [e.target.name] : e.target.value
        })
    }

    const validate = () => {
        const newErrors = {}
        const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?:{}|<>]).{6,}$/

        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
            newErrors.email = "Invalid email format"
        }

        if (formData.password.length < 6) {
            newErrors.password = "Password must be at least 6 characters"
        }

        if (!passwordRegex.test(formData.password)) {
            newErrors.password = "Password must have at least one uppercase letter, one number, and one special character.";
        }

        if (formData.password !== formData.confirmPassword) {
            newErrors.confirmPassword = "Passwords do not match"
        }

        return newErrors
    }


    return(
        <div className="register-card">
            <h2>Create Account</h2>
            <form className='register-form'>
                <label htmlFor="username">Username</label>
                <input type="text" id="username" name="username" value={formData.username} 
                placeholder="Enter your username" onChange={handleInput} required />

                <label htmlFor="email">Email</label>
                <input type="email" id="email" name="email" value={formData.email} 
                placeholder="Enter your email" onChange={handleInput} required />

                <label htmlFor="password">Password</label>
                <input type="password" id="password" name="password" value={formData.password} 
                placeholder="Enter your password" onChange={handleInput} required />

                <label htmlFor="confirmPassword">Confirm Password</label>
                <input type="password" id="confirmPassword" name="confirmPassword" 
                value={formData.confirmPassword} placeholder="Confirm your password" 
                onChange={handleInput} required />

                <button type="submit">Register</button>
            </form>
            <p className="redirect">
                Already have an account? <a href="/login">Log In</a>
            </p>
        </div>
    )
}
export default Register;