import { useNavigate } from "react-router-dom"
import { useAuth } from "../../AuthContext"
import "./Hero.css"

function Hero() {
    const { currentUser } = useAuth()
    const navigate = useNavigate()

    const handleHeroClick = () => {
        if(currentUser) {
            // go to all recipes
            return
        }

        navigate("/register")
    }

    return (
        <section className="hero">
            <div className="hero_content">
                <h1>Your recipes, your way.</h1>
                
                <p>
                    Create, discover and organize your favorite recipes in one place.
                </p>

                <button className="hero_btn" onClick={handleHeroClick}>
                    {currentUser ? "Explore Recipes" : "Get Started"}
                </button>
            </div>

            <div className="hero_image">
                <img 
                    src="/public/images/hero-food.jpg"
                    alt="Delicious food"
                />
            </div>
        </section>
    )
}
export default Hero