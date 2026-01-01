import './Header.css'
import { Link, useNavigate } from "react-router-dom"
import { LogoutUser } from "../services/UserService"
import { useAuth } from '../AuthContext'

function Header() {

    const navigate = useNavigate()
    const {currentUser, setCurrentUser} = useAuth()

    const handleLogOut = async () => {
         
        try{
        
            const response = await LogoutUser()
            setCurrentUser(null)
            navigate("/")
        
        
            }catch(error) {
                console.error(error)
                alert(error.response?.data?.detail || "LogOut failed")
            }
    }

    return(
        <header>
            <nav>
                {currentUser && (
                    <div className="user-info">
                        <img 
                            src="./images/user-icon.png"
                            alt="User Avatar"
                            className="user-avatar"
                        />
                        <span className="username">{currentUser.username}</span>
                    </div>
                )}
                <div className="nav-links">
                    <Link to="/">Home</Link>
                    <Link to="/about">About</Link>
                    {currentUser ? (
                        <>
                        {currentUser.role === "admin" ? 
                        <Link to="/adminDashboard">Dashboard</Link>
                        : <Link to="/dashboard">Dashboard</Link>
                        }
                        <Link onClick={handleLogOut}>Log out</Link>
                        </>
                    ):
                    (
                        <Link to="/login">Log In</Link>
                    )}
                </div>
            </nav>
        </header>
    )

}
export default Header