import NavBarComp from "../utils/NavbarComp"
import PlayerScoutingTop from "./PlayerScoutingTop";
import PlayerScoutingJungle from "./PlayerScoutingJungle";
import PlayerScoutingMidlane from "./PlayerScoutingMidlane";
import PlayerScoutingADC from "./PlayerScoutingADC";
import PlayerScoutingSupport from "./PlayerScoutingSupport";
import "../../styles/Scouting.css"

import { useState } from "react";

import { ThemeProvider, createTheme, Typography } from "@mui/material";
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import { grey } from '@mui/material/colors/'

const theme = createTheme({
    palette: {
        primary : {
            main: '#fff',
        }
    },
    action: {
        active: grey
    }
})

function ScoutingPlayer() {
    const [value, setValue] = useState(0)

    const handleChange = (_, newValue) => {
        setValue(newValue);
    }

    return (
        <div className="wrapper-scouting-player">
            <NavBarComp/>
            <Typography id="scouting-player-title" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold", mb: 10}}>
                Scouting Players
            </Typography>

            <Box sx={{ borderBottom: 2, borderColor: 'gray', width: 468}}> 
                <ThemeProvider theme={theme}>
                    <Tabs
                        value={value}
                        onChange={handleChange}
                        textColor="primary"
                        indicatorColor="primary"
                    >
                        <Tab
                            label="Toplane"
                            sx={{
                                color:"gray"
                            }}
                        />
                        <Tab
                            label="Jungle"
                            sx={{
                                color:"gray"
                            }}
                        />
                        <Tab
                            label="Midlane"
                            sx={{
                                color:"gray"
                            }}
                        />
                        <Tab
                            label="ADC"
                            sx={{
                                color:"gray"
                            }}
                        />
                        <Tab
                            label="Support"
                            sx={{
                                color:"gray"
                            }}
                        />
                    </Tabs>
                </ThemeProvider>
            </Box>
            <PlayerScoutingTop value={value} panelIndex={0}/>
            <PlayerScoutingJungle value={value} panelIndex={1}/>
            <PlayerScoutingMidlane value={value} panelIndex={2}/>
            <PlayerScoutingADC value={value} panelIndex={3}/>
            <PlayerScoutingSupport value={value} panelIndex={4}/>
        </div>
    )
}

export default ScoutingPlayer