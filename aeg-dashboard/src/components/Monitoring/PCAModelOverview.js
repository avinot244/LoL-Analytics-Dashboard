import NavBarComp from "../NavbarComp";
import "../../styles/PCAModelOverview.css"
import PCAModelList from "./PCAModelList";

export default function PCAModelOverview() {
    

    

    return (
        <div className="pca-model-overview-wrapper">
            <NavBarComp/>

            <h1>Manage Behavior Analysis Models</h1>
            
            <PCAModelList/>

        </div>

    )
}