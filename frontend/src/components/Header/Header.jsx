import { Link } from "react-router-dom"
import './Header.css'

function Header() {

    return(
        <header>
            <nav>
                <Link to="/">Home</Link>
                <Link to="/about">About</Link>
                <Link to="/login">Log In</Link>
            </nav>
        </header>
    )

}
export default Header