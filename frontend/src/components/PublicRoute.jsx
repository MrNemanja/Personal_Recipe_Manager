import { Navigate } from "react-router-dom";

export function PublicRoute({ currentUser, authChecked, children }) {

  if (!authChecked) return null

  if (currentUser) {
    if (currentUser.role === "admin") {
      return <Navigate to="/adminDashboard" replace />
    }
    return <Navigate to="/dashboard" replace />
  }

  return children
}