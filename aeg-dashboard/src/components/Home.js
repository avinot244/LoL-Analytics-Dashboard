import NavBarComp from "./NavbarComp"
import "../styles/Home.css"

function Home(){
    return(
        <div className="wrapper-home">
            <NavBarComp />
            <h1> This is the home page </h1>
        </div>
        
    )
}

export default Home