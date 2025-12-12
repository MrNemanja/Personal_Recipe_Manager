import {BrowserRouter as Router, Route, Routes} from "react-router-dom"
import './App.css'
import Header from './components/Header/Header'
import Home from './components/Home/Home'
import About from './components/About/About'
import LogIn from './components/LogIn/LogIn'
import Register from './components/Register/Register'
import Dashboard from './components/Dashboard/Dashboard'
import Footer from './components/Footer/Footer'

function App() {

  return (
    <Router>
      <div className="app-container">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/login" element={<LogIn />} />
            <Route path="/register" element={<Register />} />
            <Route path="/dashboard" element={<Dashboard />} />  
          </Routes>  
        </main>
        <Footer />
      </div>
    </Router>
  )
}

export default App
