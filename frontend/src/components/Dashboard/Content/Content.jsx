import Stats from "./Stats/Stats"
import MyRecipes from "./MyRecipes/MyRecipes"
import Favorites from "./Favorites/Favorites"
import CreateRecipe from "./CreateRecipe/CreateRecipe"
import "./Content.css"

function Content({ activeSection }) {
    return(
        <div className="main_content">

            <div className="dashboard_header">
                <div className="welcome">
                    <h2>Welcome back, Nemanja! 👋</h2>
                    <p>Here's what's happening with your recipes.</p>
                </div>
                
                <Stats />
            </div>            

            {activeSection === "my-recipes" && <MyRecipes />}
            {activeSection === "favorites" && <Favorites />}
            {activeSection === "create" && <CreateRecipe />}

        </div>
    )
}
export default Content