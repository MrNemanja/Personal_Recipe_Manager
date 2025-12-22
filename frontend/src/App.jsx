import {BrowserRouter as Router, Route, Routes} from "react-router-dom"
import { useState, useEffect } from "react"
import { getCurrentUser } from "./components/services/UserService"
import './App.css'
import Header from './components/Header/Header'
import Home from './components/Home/Home'
import About from './components/About/About'
import LogIn from './components/LogIn/LogIn'
import Register from './components/Register/Register'
import Dashboard from './components/Dashboard/Dashboard'
import AdminDashboard from "./components/AdminDashboard/AdminDashboard"
import Footer from './components/Footer/Footer'
import { ProtectedRoute } from "./components/ProtectedRoute"
import { PublicRoute } from "./components/PublicRoute"

function App() {

  const [currentUser, setCurrentUser] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
        
    const fetchUser = async () => {
        
        try{
          
          const response = await getCurrentUser();
          setCurrentUser(response)
      
        }catch(error) {
            setCurrentUser(null)
        }
        finally{
            setLoading(true)
        }
    }
    fetchUser()
      
  },[])

  return (
    <>
    <Router>
      <div className="app-container">
        <Header currentUser={currentUser} setCurrentUser={setCurrentUser}/>
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/login" element={
              <PublicRoute currentUser={currentUser} loading={loading}>
              <LogIn setCurrentUser={setCurrentUser} />
              </PublicRoute>
              } />
            <Route path="/register" element={
              <PublicRoute currentUser={currentUser} loading={loading}>
              <Register />
              </PublicRoute>
              } />
            <Route path="/dashboard" element={
              <ProtectedRoute currentUser={currentUser} loading={loading} requiredRole={"regularUser"}>
              <Dashboard currentUser={currentUser} />
              </ProtectedRoute>
              } />  
            <Route path="/adminDashboard" element={
              <ProtectedRoute currentUser={currentUser} loading={loading} requiredRole={"admin"}>
              <AdminDashboard currentUser={currentUser} />
              </ProtectedRoute>
              } />  
          </Routes>  
        </main>
        <Footer />
      </div>
    </Router>
    </>
  )
}

export default App
