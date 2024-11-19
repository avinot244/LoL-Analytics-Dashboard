import NavBarComp from "../utils/NavbarComp"
import "../../styles/Home.css"
import TopMetaPicksPanel from "./TopMetaPicksPanel";
import LatestDraftsPanel from "./LatestDraftsPanel";
import { useContext } from "react";

import { useState } from "react";
import { ThemeProvider, createTheme, Typography } from "@mui/material";
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import { grey } from '@mui/material/colors/'

import AuthContext from "../context/AuthContext";



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


function Home({loggedIn, setLoggedIn}){
    const [value, setValue] = useState(0)

    const handleChange = (_, newValue) => {
        setValue(newValue);
    }

    return(
        <div className="wrapper-overview">
            <NavBarComp loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>
            <Typography id="PCAdocumentation-title" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold"}}>
                Home Page
            </Typography>
            <Box sx={{ borderBottom: 2, borderColor: 'gray', width: 290}}> 
            <ThemeProvider theme={theme}>
                <Tabs
                    value={value}
                    onChange={handleChange}
                    textColor="primary"
                    indicatorColor="primary"
                >
                    <Tab
                        label="Top Meta Picks"
                        sx={{
                            color:"gray"
                        }}
                    />
                    <Tab
                        label="Latest Drafts"
                        sx={{
                            color:"gray"
                        }}
                    />
                </Tabs>
            </ThemeProvider>
            </Box>
            <TopMetaPicksPanel value={value} panelIndex={0}/>
            <LatestDraftsPanel value={value} panelIndex={1}/>
        </div>
    )
}

export default Home