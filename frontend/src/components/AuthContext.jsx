import { createContext, useContext, useState, useEffect } from "react";
import { getCurrentUser } from "./services/UserService";
import { Children } from "react";

const AuthContext = createContext()

export const AuthProvider = ({children}) => {

  const [currentUser, setCurrentUser] = useState(null)
  const [authChecked, setAuthChecked] = useState(false)

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await getCurrentUser()
        setCurrentUser(response)
      } catch (error) {
        setCurrentUser(null)
      } finally {
        setAuthChecked(true)
      }
    };
    fetchUser()
  }, [])

  return (
    <AuthContext.Provider value={{ currentUser, setCurrentUser, authChecked }}>
      {children}
    </AuthContext.Provider>
  )

}

export const useAuth = () => useContext(AuthContext)
