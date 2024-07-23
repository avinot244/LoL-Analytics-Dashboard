import NavBarComp from "../utils/NavbarComp";
import "../../styles/PCAModelOverview.css"
import PCAModelList from "./PCAModelList";
import RedirectPage from "../Home/RedirectPage";

import { Typography } from "@mui/material";

export default function PCAModelOverview() {
    return (
        <div className="pca-model-overview-wrapper">
            <NavBarComp/>
            
            <Typography id="PCAdocumentation-title" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold", mb: 10}}>
                Manage Behavior Analysis Models
            </Typography>

            <PCAModelList/>
        </div>
    )
}