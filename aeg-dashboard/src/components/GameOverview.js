import NavBarComp from "./NavbarComp"
import "../styles/GameOverview.css"

function GameOverview(){
    return(
        <div className="wrapper-overview-game">
            <NavBarComp />
            <h1> This is the home page </h1>
        </div>
        
    )
}

export default GameOverview