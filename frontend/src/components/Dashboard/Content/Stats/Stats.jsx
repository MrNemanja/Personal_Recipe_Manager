import "./Stats.css"

function Stats() {
    return (
        <div className="stats">
            <div className="stat_card">
                <span>🍳</span>
                <div>
                    <strong>12</strong>
                    <p>My Recipes</p>
                </div>
            </div>
            <div className="stat_card">
                <span>❤️</span>
                <div>
                    <strong>5</strong>
                    <p>Favorites</p>
                </div>
            </div>
        </div>
    )
}
export default Stats