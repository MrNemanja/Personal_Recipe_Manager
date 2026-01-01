import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

function PublicRoute({ children }) {

  const {currentUser, authChecked} = useAuth()

  if (!authChecked) return null

  if (currentUser) {
    if (currentUser.role === "admin") {
      return <Navigate to="/adminDashboard" replace />
    }
    return <Navigate to="/dashboard" replace />
  }

  return children
}
export default PublicRoute