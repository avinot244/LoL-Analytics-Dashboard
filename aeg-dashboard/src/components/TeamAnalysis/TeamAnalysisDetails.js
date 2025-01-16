import { Typography } from "@mui/material"

import NavBarComp from "../utils/NavbarComp"

import "../../styles/TeamAnalysisDetails.css"

function TeamAnalysisDetails() {
    return (
        <div className="wrapper-teamAnalysisDetails">
            <NavBarComp/>
            <Typography id="teamAnalysisDetails-title" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold", mb: 10}}>
                Team Analysis Details
            </Typography>
        </div>
    )
}

export default TeamAnalysisDetails