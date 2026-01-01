import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

function ProtectedRoute({ requiredRole, children }) {

  const {currentUser, authChecked} = useAuth()

  if (!authChecked) return null

  if (!currentUser) {
    return <Navigate to="/login" replace />
  }

  if (requiredRole && currentUser.role !== requiredRole) {
    return <Navigate to="/" replace />
  }

  return children
}
export default ProtectedRoute