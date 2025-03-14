import NavBarComp from "../utils/NavbarComp";
import ChampionOverviewPanel from "./ChampionOverviewPanel"
import "../../styles/ChampionOverview.css"
import SearchComp from "../utils/SearchComp";

import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';

import {grey} from '@mui/material/colors/'

import { useState, useEffect, useContext } from "react";
import { ThemeProvider, createTheme, Typography } from "@mui/material";

import { API_URL } from "../../constants";

import Button from "@mui/material/Button"
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import RedirectPage from "../Home/RedirectPage";
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


function ChampionOverviewScrim() {
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
    let {authTokens} = useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }

    const fetchPatchListFromTournament = async (tournament) => {
        const result = await fetch(API_URL + `dataAnalysis/patch/getFromTournament/${tournament}/`, {
            method: "GET",
            headers:header
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
            <NavBarComp/>
            <Typography id="PCAdocumentation-title" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold"}}>
                Champion Overview
            </Typography>

            <div className="dashboard-champOverview-controlPannel">
                <ul className="dashboard-champOverview-controlPannel-list">
                    <li>
                        <SearchComp
                            defaultValue={""}
                            elementList={side}
                            setSelectedElement={setActiveSide}
                            label={"side"}
                            width={120}
                        />
                    </li>
                    <li>
                        <SearchComp
                            elementList={patchList}
                            defaultValue={activePatch}
                            setSelectedElement={setActivePatch}
                            label={"patch"}
                            width={140}
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