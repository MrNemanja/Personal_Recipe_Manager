import { useState } from "react"
import Content from "./Content/Content"
import Sidebar from "./Sidebar/Sidebar"
import "./Dashboard.css"

function Dashboard() {

    const [activeSection, setActiveSection] = useState("my-recipes")

    return(
        <div className="dashboard">
            <Sidebar
                activeSection={activeSection}
                setActiveSection={setActiveSection}
            />
            <Content 
                activeSection={activeSection}
            />
        </div>
    )
}
export default Dashboard