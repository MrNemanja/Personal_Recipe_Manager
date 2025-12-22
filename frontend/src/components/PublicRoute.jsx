import { Navigate } from "react-router-dom";

export function PublicRoute({ currentUser, loading, children }) {

  if (!loading) return null

  if (currentUser) {
    if (currentUser.role === "admin") {
      return <Navigate to="/adminDashboard" replace />
    }
    return <Navigate to="/dashboard" replace />
  }

  return children
}