import "./Sidebar.css"

function Sidebar({ activeSection, setActiveSection }) {
    return(
            <div className="menu">
                <div className="menu_brand">
                    <span>🍴</span>
                    <h2>Recipe Manager</h2>
                </div>

                <p className="menu_section_title">YOUR KITCHEN</p>
                <br/>

                <div className="menu_buttons">
                    <button 
                        className={`menu_btn ${activeSection === "my-recipes" ? "active" : ""}`}
                        onClick={() => setActiveSection("my-recipes")}
                    >
                        🍳 My Recipes
                    </button>

                    <button 
                        className={`menu_btn ${activeSection === "favorites" ? "active" : ""}`}
                        onClick={() => setActiveSection("favorites")}
                    >
                        ❤️ Favorites
                    </button>

                    <button 
                        className={`menu_btn ${activeSection === "create" ? "active" : ""}`}
                        onClick={() => setActiveSection("create")}
                    >
                        ➕ Create
                    </button>
                </div>
            </div>
    ) 
}
export default Sidebar