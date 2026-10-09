import Hero from "./Hero/Hero"
import RecipeOfTheDay from "./RecipeOfTheDay/RecipeOfTheDay"
import ExploreRecipes from "./ExploreRecipes/ExploreRecipes"

function Home() {

    return(
        <main className="home_content">
            <Hero />
            <RecipeOfTheDay />
            <ExploreRecipes />
        </main>
    )
}
export default Home