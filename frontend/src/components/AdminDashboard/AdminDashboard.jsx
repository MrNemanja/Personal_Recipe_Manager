import { useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../AuthContext"

function AdminDashboard() {

    const navigate = useNavigate()
    const { currentUser } = useAuth()
    
    useEffect(() => {
            
        if (currentUser) {
            if (currentUser.role === "regularUser") navigate("/dashboard")
        }
        else navigate("/login")
          
    },[currentUser])
    
    return(
        <></>
    )
}
export default AdminDashboard