import NavBarComp from "./NavbarComp"
import "../styles/PlayerOverview.css"

function PlayerOverview(){
    return(
        <div className="wrapper-overview">
            <NavBarComp />
            <h1> Player Overview </h1>
        </div>
        
    )
}

export default PlayerOverview