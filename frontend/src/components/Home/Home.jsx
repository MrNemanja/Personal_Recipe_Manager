import Hero from "./Hero/Hero"
import RecipeOfTheDay from "./RecipeOfTheDay/RecipeOfTheDay"

function Home() {

    return(
        <main className="home_content">
            <Hero />
            <RecipeOfTheDay />
        </main>
    )
}
export default Home