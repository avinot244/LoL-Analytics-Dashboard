import NavBarComp from "./NavbarComp";
import ChampionOverviewPanel from "./ChampionOverviewPanel"
import "../styles/ChampionOverview.css"

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

    const handleChange = (event, newValue) => {
        setValue(newValue);
    }

    return(
        <div className="wrapper-overview">
            <NavBarComp />
            <h1> Champion overview </h1>
            <Box sx={{ borderBottom: 1, borderColor: 'black', width: 468}}> 
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
        
            
            <ChampionOverviewPanel value={value} panelIndex={0}/>
            <ChampionOverviewPanel value={value} panelIndex={1}/>
            <ChampionOverviewPanel value={value} panelIndex={2}/>
            <ChampionOverviewPanel value={value} panelIndex={3}/>
            <ChampionOverviewPanel value={value} panelIndex={4}/>
        </div>
    )
}


export default ChampionOverview