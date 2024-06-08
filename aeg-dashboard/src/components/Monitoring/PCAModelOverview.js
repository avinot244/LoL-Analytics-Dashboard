import NavBarComp from "../NavbarComp";
import "../../styles/PCAModelOverview.css"
import PCAModelList from "./PCAModelList";
import RedirectPage from "../Home/RedirectPage";

export default function PCAModelOverview({loggedIn, setLoggedIn}) {
    return (
        <div className="pca-model-overview-wrapper">
            {
                loggedIn ? (
                    <>
                        <NavBarComp loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>

                        <h1>Manage Behavior Analysis Models</h1>

                        <PCAModelList/>
                    </>
                ) : (
                    <RedirectPage />
                )
            }
        </div>
    )
}