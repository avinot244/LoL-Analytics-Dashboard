import NavBarComp from "../utils/NavbarComp";
import "../../styles/PCAModelOverview.css"
import PCAModelList from "./PCAModelList";
import RedirectPage from "../Home/RedirectPage";

export default function PCAModelOverview({loggedIn, setLoggedIn}) {
    return (
        <div className="pca-model-overview-wrapper">
            <NavBarComp loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>

            <h1>Manage Behavior Analysis Models</h1>

            <PCAModelList/>
        </div>
    )
}