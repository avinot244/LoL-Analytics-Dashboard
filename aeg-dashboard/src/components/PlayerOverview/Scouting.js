import NavBarComp from "../utils/NavbarComp";
import "../../styles/Scouting.css"

import { Typography } from "@mui/material";


function ScoutingPlayer() {
    return (
        <div className="wrapper-scouting-player">
            <NavBarComp/>
            <Typography id="scouting-player-title" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold", mb: 10}}>
                Scouting Players
            </Typography>
        </div>
    )
}

export default ScoutingPlayer