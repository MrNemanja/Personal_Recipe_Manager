import { Navigate } from "react-router-dom";

export function ProtectedRoute({ currentUser, loading, requiredRole, children }) {

  if (!loading) return null

  if (!currentUser) {
    return <Navigate to="/login" replace />
  }

  if (requiredRole && currentUser.role !== requiredRole) {
    return <Navigate to="/" replace />
  }

  return children
}