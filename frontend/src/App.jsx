import './App.css'
import 'react-toastify/dist/ReactToastify.css'
import {BrowserRouter as Router, Route, Routes} from "react-router-dom"
import { useState, useEffect } from "react"
import { getCurrentUser } from "./components/services/UserService"
import Header from './components/Header/Header'
import Home from './components/Home/Home'
import About from './components/About/About'
import LogIn from './components/LogIn/LogIn'
import Register from './components/Register/Register'
import Dashboard from './components/Dashboard/Dashboard'
import AdminDashboard from "./components/AdminDashboard/AdminDashboard"
import Footer from './components/Footer/Footer'
import VerifyEmail from './components/VerifyEmail/VerifyEmail'
import ResendVerification from './components/ResendVerification/ResendVerification'
import ForgotPassword from './components/ForgotPassword/ForgotPassword'
import ResetPassword from './components/ResetPassword/ResetPassword'
import { ProtectedRoute } from "./components/ProtectedRoute"
import { PublicRoute } from "./components/PublicRoute"
import { ToastContainer } from "react-toastify";


function App() {

  const [currentUser, setCurrentUser] = useState(null)
  const [authChecked, setAuthChecked] = useState(false)

  useEffect(() => {
        
    const fetchUser = async () => {
        
        try{
          
          const response = await getCurrentUser();
          setCurrentUser(response)
      
        }catch(error) {
            setCurrentUser(null)
        }
        finally{
            setAuthChecked(true)
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
              <PublicRoute currentUser={currentUser} authChecked={authChecked}>
              <LogIn setCurrentUser={setCurrentUser} />
              </PublicRoute>
              } />
            <Route path="/register" element={
              <PublicRoute currentUser={currentUser} authChecked={authChecked}>
              <Register />
              </PublicRoute>
              } />
            <Route path="/dashboard" element={
              <ProtectedRoute currentUser={currentUser} authChecked={authChecked} requiredRole={"regularUser"}>
              <Dashboard currentUser={currentUser} />
              </ProtectedRoute>
              } />  
            <Route path="/adminDashboard" element={
              <ProtectedRoute currentUser={currentUser} authChecked={authChecked} requiredRole={"admin"}>
              <AdminDashboard currentUser={currentUser} />
              </ProtectedRoute>
              } />
            <Route path="/verify-email" element={<VerifyEmail />} />
            <Route path="/resend-verification" element={<ResendVerification />} />
            <Route path='/forgot-password' element={<ForgotPassword />} />
            <Route path='/reset-password' element={<ResetPassword />} />    
          </Routes>  
        </main>
        <Footer />
      </div>
    </Router>
    <ToastContainer 
      position="top-right"
      autoClose={3000}
      hideProgressBar={false}
      newestOnTop={false}
      closeOnClick
      rtl={false}
      pauseOnFocusLoss
      draggable
      pauseOnHover
    />
    </>
  )
}

export default App
