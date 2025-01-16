import { Typography } from "@mui/material"

import NavBarComp from "../utils/NavbarComp"

import "../../styles/TeamAnalysisOverall.css"

function TeamAnalysisOverall() {
    return (
        <div className="wrapper-teamAnalysisOverall">
            <NavBarComp />
            <Typography id="teamAnalysisOverall-title" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold", mb: 10}}>
                Team Analysis Overall
            </Typography>
        </div>
    )
}

export default TeamAnalysisOverall