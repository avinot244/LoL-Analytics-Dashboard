import NavBarComp from "../NavbarComp"
import "../../styles/GameOverview.css"
import SearchComp from "../SearchComp"

import Stack from '@mui/material/Stack'
import Button from "@mui/material/Button"
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import { useState } from "react"

function GameOverview(){


    const gameList = [
        {label: "SCRIM G1 AEG vs GO", value:"scrim_g1_aeg_vs_go"},
        {label: "SCRIM G2 AEG vs GO", value:"scrim_g2_aeg_vs_go"},
        {label: "SCRIM G3 AEG vs GO", value:"scrim_g3_aeg_vs_go"},
        {label: "ESPORTs G1 G2 vs FNC", value:"esports_g1_g2_vs_fnc"},
        {label: "ESPORTs G2 G2 vs FNC", value:"esports_g2_g2_vs_fnc"},
        {label: "ESPORTs G3 G2 vs FNC", value:"esports_g3_g2_vs_fnc"},
        {label: "ESPORTs G4 G2 vs FNC", value:"esports_g4_g2_vs_fnc"},
        {label: "ESPORTs G5 G2 vs FNC", value:"esports_g5_g2_vs_fnc"}

    ]
    const [selectedGame, setSelectedGame] = useState('')

    return(
        <div className="wrapper-overview-game">
            <NavBarComp />
            <h1> Game overview </h1>
            <br/>
            <Stack spacing={2} direction="row" justifyContent="center">
                <SearchComp 
                    label={"Games"}
                    elementList={gameList}
                    setSelectedElement={setSelectedGame}
                />
                <Button 
                    variant="contained" 
                    endIcon={<ArrowForwardIosIcon />}>
                
                    Analyze
                
                </Button>
                
            </Stack>
            <p>{selectedGame.value}</p>
        </div>
        
    )
}

export default GameOverview