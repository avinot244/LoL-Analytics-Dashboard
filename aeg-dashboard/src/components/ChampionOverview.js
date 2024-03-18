import NavBarComp from "./NavbarComp";
import ChampionOverviewPanel from "./ChampionOverviewPanel"
import "../styles/ChampionOverview.css"
import SelectComp from "./SelectComp";

import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';

import { amber,  brown,  grey} from '@mui/material/colors/'

import { useState } from "react";
import { ThemeProvider, createTheme } from "@mui/material";

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


function ChampionOverview() {
    const [value, setValue] = useState(0)
    const patchList = [1.4, 1.14];
    const side = ["Blue", "Red", "Both"];
    const tournamentList = ["Tournament 1", "Tournament 2"];
    const [activePatch, setActivePatch] = useState('Select a patch')
    const [activeSide, setActiveSide] = useState('Select a side')
    const [activeTournament, setActiveTournament] = useState("Select a tournament")

    const handleChange = (event, newValue) => {
        setValue(newValue);
    }

    return(
        <div className="wrapper-overview">
            <NavBarComp />
            <h1> Champion overview </h1>

            <div className="dashboard-champOverview-controlPannel">
                <ul className="dashboard-champOverview-controlPannel-list">
                    <li>
                        <SelectComp 
                            elementList={patchList}
                            defaultValue={"-- Patch --"}
                            setActive={setActivePatch}/>
                    </li>
                    <li>
                        <SelectComp
                            elementList={side}
                            defaultValue={"-- Side --"}
                            setActive={setActiveSide}/>
                    </li>
                    <li>
                        <SelectComp 
                            elementList={tournamentList}
                            defaultValue={"-- Tournament --"}
                            setActive={setActiveTournament}/>
                    </li>
                </ul>
            </div>


            <Box sx={{ borderBottom: 2, borderColor: 'gray', width: 574}}> 
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
                    <Tab 
                        label="All Roles"
                        sx={{
                            color:"gray"
                        }}
                    />
                </Tabs>
            </ThemeProvider>
            </Box>
        
            
            <ChampionOverviewPanel value={value} panelIndex={0}/>
            <ChampionOverviewPanel value={value} panelIndex={1}/>
            <ChampionOverviewPanel value={value} panelIndex={2}/>
            <ChampionOverviewPanel value={value} panelIndex={3}/>
            <ChampionOverviewPanel value={value} panelIndex={4}/>
            <ChampionOverviewPanel value={value} panelIndex={5}/>
        </div>
    )
}


export default ChampionOverview