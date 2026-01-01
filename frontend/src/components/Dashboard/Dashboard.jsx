import { useEffect } from "react"
import { useNavigate } from "react-router-dom"
import { useAuth } from "../AuthContext"

function Dashboard() {

    const navigate = useNavigate()
    const { currentUser } = useAuth()
    
    useEffect(() => {
                
        if (currentUser) {
            if (currentUser.role === "admin") navigate("/adminDashboard")
        }
        else navigate("/login")
              
    },[currentUser])

    return(
        <></>
    )
}
export default Dashboard