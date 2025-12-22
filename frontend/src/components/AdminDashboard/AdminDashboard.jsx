import { useEffect } from "react"
import { useNavigate } from "react-router-dom"

function AdminDashboard({currentUser}) {

    const navigate = useNavigate()

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