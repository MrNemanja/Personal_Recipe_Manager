import { Navigate } from "react-router-dom";

export function ProtectedRoute({ currentUser, authChecked, requiredRole, children }) {

  if (!authChecked) return null

  if (!currentUser) {
    return <Navigate to="/login" replace />
  }

  if (requiredRole && currentUser.role !== requiredRole) {
    return <Navigate to="/" replace />
  }

  return children
}