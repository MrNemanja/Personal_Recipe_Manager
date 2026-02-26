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
        full_name: "",
        phone: "",
        city: "",
        country: "",
        dob: "",
        profile_image: null
    })
    const [errors, setErrors] = useState({})
    const navigate = useNavigate()


    const handleInput = (e) => {
        setFormData({
            ...formData,
            [e.target.name] : e.target.files? e.target.files[0] : e.target.value
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

        const dataToSend = new FormData()

        dataToSend.append("username", formData.username)
        dataToSend.append("email", formData.email)
        dataToSend.append("password", formData.password)
        dataToSend.append("full_name", formData.full_name)
        dataToSend.append("phone", formData.phone)
        dataToSend.append("city", formData.city)
        dataToSend.append("country", formData.country)

        if (formData.dob) {
            dataToSend.append("dob", formData.dob)
        }

        if(formData.profile_image) {
            dataToSend.append("profile_image", formData.profile_image)
        }

        try{
            const response = await RegisterUser(dataToSend)
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

                <label htmlFor="full_name">Full Name</label>
                <input type="text" id="full_name" name="full_name" value={formData.full_name} 
                placeholder="Enter your full name" onChange={handleInput} />

                <label htmlFor="phone">Phone</label>
                <input type="text" id="phone" name="phone" value={formData.phone} 
                placeholder="Enter your phone" onChange={handleInput} />

                <label htmlFor="city">City</label>
                <input type="text" id="city" name="city" value={formData.city} 
                placeholder="Enter your city" onChange={handleInput} />

                <label htmlFor="country">Country</label>
                <input type="text" id="country" name="country" value={formData.country} 
                placeholder="Enter your country" onChange={handleInput} />

                <label htmlFor="dob">Date of birth</label>
                <input type="date" id="dob" name="dob" value={formData.dob} 
                onChange={handleInput} />

                <label htmlFor="profile_image">Profile Image</label>
                <input type="file" id="profile_image" name="profile_image" 
                onChange={handleInput} />

                <button type="submit">Register</button>
            </form>
            <p className="redirect">
                Already have an account? <a href="/login">Log In</a>
            </p>
            
        </div>
    )
}
export default Register;