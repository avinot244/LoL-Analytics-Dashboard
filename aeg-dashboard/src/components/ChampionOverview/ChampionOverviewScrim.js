import NavBarComp from "../utils/NavbarComp";
import ChampionOverviewPanel from "./ChampionOverviewPanel"
import "../../styles/ChampionOverview.css"
import SelectComp from "../utils/SelectComp";

import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';

import {grey} from '@mui/material/colors/'

import { useState, useEffect } from "react";
import { ThemeProvider, createTheme } from "@mui/material";

import { API_URL } from "../../constants";

import Button from "@mui/material/Button"
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import RedirectPage from "../Home/RedirectPage";

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


function ChampionOverviewScrim({loggedIn, setLoggedIn}) {
    const [patchList, setPatchList] = useState([]);
    const [value, setValue] = useState(0)
    const side = ["Blue", "Red", "Both"];
    const [displayFlag, setDisplayFlag] = useState(false)
    const [displayPatchFlag, setDisplayPatchFlag] = useState(true)


    const [activePatch, setActivePatch] = useState()
    const [activeSide, setActiveSide] = useState('Blue')

    const activeTournament = "League of Legends Scrims"


    const handleChange = (event, newValue) => {
        setValue(newValue);
    }

    const fetchPatchListFromTournament = async (tournament) => {
        const result = await fetch(API_URL + `dataAnalysis/patch/getFromTournament/${tournament}/`, {
            method: "GET"
        })
        result.json().then(result => {
            const newPatchList = result;
            setPatchList(newPatchList)
            setActivePatch(newPatchList[newPatchList.length - 1])
        })
    }

    

    useEffect(() => {
        fetchPatchListFromTournament(activeTournament)
    }, [])

    return(
        <div className="wrapper-champOverview">
            <NavBarComp loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>
            <h1> Champion overview </h1>

            <div className="dashboard-champOverview-controlPannel">
                <ul className="dashboard-champOverview-controlPannel-list">
                    <li>
                        <SelectComp
                            elementList={side}
                            defaultValue={activeSide}
                            setActive={setActiveSide}/>
                    </li>
                    <li>
                        <SelectComp 
                            elementList={patchList}
                            defaultValue={activePatch}
                            setActive={setActivePatch}
                        />
                    </li>
                    <li>
                        <Button 
                            variant="contained" 
                            endIcon={<ArrowForwardIosIcon />}
                            onClick={() => {
                                setDisplayFlag(true)
                                
                            }}    
                        >
                            Analyze
                        </Button>
                    </li>
                    <li>
                        <Button 
                            variant="contained" 
                            endIcon={<RestartAltIcon />}
                            onClick={() => {
                                setDisplayFlag(false)
                                setDisplayPatchFlag(false)
                            }}    
                        >
                            Reset
                        </Button>
                    </li>
                </ul>   
            </div>

            {
                displayFlag ?
                <div className="dashboard-champOverview-rolePanel">
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
                    <ChampionOverviewPanel value={value} panelIndex={0} tournament={activeTournament} patch={activePatch} side={activeSide}/>
                    <ChampionOverviewPanel value={value} panelIndex={1} tournament={activeTournament} patch={activePatch} side={activeSide}/>
                    <ChampionOverviewPanel value={value} panelIndex={2} tournament={activeTournament} patch={activePatch} side={activeSide}/>
                    <ChampionOverviewPanel value={value} panelIndex={3} tournament={activeTournament} patch={activePatch} side={activeSide}/>
                    <ChampionOverviewPanel value={value} panelIndex={4} tournament={activeTournament} patch={activePatch} side={activeSide}/>
                    <ChampionOverviewPanel value={value} panelIndex={5} tournament={activeTournament} patch={activePatch} side={activeSide}/>
                </div>
                :
                <div className="alt">

                </div>
            }
        </div>
    )
}


export default ChampionOverviewScrim