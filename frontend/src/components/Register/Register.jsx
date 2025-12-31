import './Register.css'
import { RegisterUser } from '../services/UserService'
import {useState, useEffect} from 'react'
import { useNavigate } from 'react-router-dom'

function Register() {
    
    const [formData, setFormData] = useState({
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
        role: "regularUser"
    })
    const [errors, setErrors] = useState({})
    const navigate = useNavigate()


    const handleInput = (e) => {
        setFormData({
            ...formData,
            [e.target.name] : e.target.value
        })
    }

    const validate = () => {

        const newErrors = {}
        const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?:{}|<>]).{6,}$/
        const emailRegex = /^[^\s@]+@[^\s@]+\.[a-zA-Z]{2,}(\.[a-zA-Z]{2,})?$/;

        if (!emailRegex.test(formData.email)) {
            newErrors.email = "Invalid email format";
        }

        if (!passwordRegex.test(formData.password)) {
            newErrors.password = "Password must have at least 6 characters, one uppercase letter, one number, and one special character.";
        }

        if (formData.password !== formData.confirmPassword) {
            newErrors.confirmPassword = "Passwords do not match"
        }

        return newErrors
    }

    const handleSubmit = async (e) => {
        
        e.preventDefault()
        
        const validationErrors = validate()
        setErrors(validationErrors)

        if(Object.keys(validationErrors).length > 0) return

        try{
            const response = await RegisterUser({
                username: formData.username,
                email: formData.email,
                password: formData.password,
                role: formData.role
            })
            alert(response.message)
            navigate("/")


        }catch(error) {
            console.error(error)
            alert(error.response?.data?.detail || "Registration failed")
        }

    }


    return(
        <div className="register-card">
            <h2>Create Account</h2>
            <form className='register-form' onSubmit={handleSubmit}>
                <label htmlFor="username">Username</label>
                <input type="text" id="username" name="username" value={formData.username} 
                placeholder="Enter your username" onChange={handleInput} required />

                <label htmlFor="email">Email</label>
                <input type="email" id="email" name="email" value={formData.email} 
                placeholder="Enter your email" onChange={handleInput} required />
                {errors.email && <p className='error'>{errors.email}</p>}

                <label htmlFor="password">Password</label>
                <input type="password" id="password" name="password" value={formData.password} 
                placeholder="Enter your password" onChange={handleInput} required />
                {errors.password && <p className='error'>{errors.password}</p>}

                <label htmlFor="confirmPassword">Confirm Password</label>
                <input type="password" id="confirmPassword" name="confirmPassword" 
                value={formData.confirmPassword} placeholder="Confirm your password" 
                onChange={handleInput} required />
                {errors.confirmPassword && <p className='error'>{errors.confirmPassword}</p>}

                <button type="submit">Register</button>
            </form>
            <p className="redirect">
                Already have an account? <a href="/login">Log In</a>
            </p>
            
        </div>
    )
}
export default Register;