import NavBarComp from "../NavbarComp"
import "../../styles/Home.css"
import TopMetaPicksPanel from "./TopMetaPicksPanel";
import LatestDraftsPanel from "./LatestDraftsPanel";

import { useState } from "react";
import { ThemeProvider, createTheme } from "@mui/material";
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import { grey } from '@mui/material/colors/'

import { useNavigate } from "react-router-dom";

import RedirectPage from "./RedirectPage";



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


function Home({loggedIn, setLoggedIn, email}){
    
    const [value, setValue] = useState(0)

    const handleChange = (event, newValue) => {
        setValue(newValue);
    }

    return(
        <div className="wrapper-overview">
            {
                loggedIn ? (
                    <>
                        <NavBarComp loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>
                        <br/>
                        <h1>Home Page</h1>

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
                    </>
                ) : (
                    <RedirectPage/>
                )
            }
            
        </div>
    )
}

export default Home