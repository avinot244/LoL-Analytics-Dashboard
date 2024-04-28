import NavBarComp from "../NavbarComp";
import ChampionOverviewPanel from "./ChampionOverviewPanel"
import "../../styles/ChampionOverview.css"
import SelectComp from "../SelectComp";

import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';

import {grey} from '@mui/material/colors/'

import { useState, useEffect } from "react";
import { ThemeProvider, createTheme } from "@mui/material";

import { API_URL } from "../../constants";

import Button from "@mui/material/Button"
import SearchIcon from '@mui/icons-material/Search';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import RestartAltIcon from '@mui/icons-material/RestartAlt';

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
    const [patchList, setPatchList] = useState([]);
    const [value, setValue] = useState(0)
    const side = ["Blue", "Red", "Both"];
    const [tournamentList, setTournamentList] = useState([])
    const [displayFlag, setDisplayFlag] = useState(false)
    const [displayPatchFlag, setDisplayPatchFlag] = useState(false)


    const [activePatch, setActivePatch] = useState('14.1')
    const [activeSide, setActiveSide] = useState('Blue')
    const [activeTournament, setActiveTournament] = useState("La Ligue Française - Spring 2024 (Regular Season: Regular Season)")


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
        })
    }

    

    useEffect(() => {
        const fetchPatchList = async () => {
            const result = await fetch(API_URL + "dataAnalysis/patch/getList", {
                method: "GET"
            })
            result.json().then(result => {
                const newPatchList = result;
                setPatchList(newPatchList);
            })
        }

        const fetchTournamentList = async () => {
            const result = await fetch(API_URL + "dataAnalysis/tournament/getList", {
                method: "GET"
            })
            result.json().then(result => {
                const newTournamentList = result.sort();
                setTournamentList(newTournamentList)
            })
        }
        
        fetchPatchList();
        fetchTournamentList();
    }, [])

    return(
        <div className="wrapper-champOverview">
            <NavBarComp />
            <h1> Champion overview </h1>

            <div className="dashboard-champOverview-controlPannel">
                <ul className="dashboard-champOverview-controlPannel-list">
                    <li>
                        <SelectComp 
                            elementList={tournamentList}
                            defaultValue={"-- Tournament --"}
                            setActive={setActiveTournament}
                        />
                        
                    </li>
                    <li>
                        <SelectComp
                            elementList={side}
                            defaultValue={"-- Side --"}
                            setActive={setActiveSide}/>
                    </li>
                    <li>
                        <Button 
                            variant="contained" 
                            endIcon={<SearchIcon />}
                            onClick={() => {
                                fetchPatchListFromTournament(activeTournament)
                                setDisplayPatchFlag(true)
                            }}    
                        >
                            Search Patches
                        </Button>
                    </li>
                </ul>

                {
                    displayPatchFlag ?
                    <ul className="dashboard-champOverview-controlPannel-list">
                        <li>
                            <SelectComp 
                                elementList={patchList}
                                defaultValue={"-- Patch --"}
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
                    :
                    <div className="alt">

                    </div>

                }
                
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


export default ChampionOverview