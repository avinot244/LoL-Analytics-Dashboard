import NavBarComp from "../utils/NavbarComp";
import ChampionOverviewPanel from "./ChampionOverviewPanel"
import "../../styles/ChampionOverview.css"
import SelectComp from "../utils/SelectComp";

import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';

import {grey} from '@mui/material/colors/'

import { useState, useEffect, useContext } from "react";
import { ThemeProvider, createTheme } from "@mui/material";

import { API_URL } from "../../constants";

import Button from "@mui/material/Button"
import SearchIcon from '@mui/icons-material/Search';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import SearchComp from "../utils/SearchComp";
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


function ChampionOverview() {
    const [patchList, setPatchList] = useState([]);
    const [value, setValue] = useState(0)
    const side = ["Blue", "Red", "Both"];
    const [tournamentList, setTournamentList] = useState([])
    const [displayFlag, setDisplayFlag] = useState(false)
    const [displayPatchFlag, setDisplayPatchFlag] = useState(false)


    const [activePatch, setActivePatch] = useState()
    const [activeSide, setActiveSide] = useState('Blue')
    const [activeTournament, setActiveTournament] = useState()

    let {authTokens} = useContext(AuthContext)


    const handleChange = (event, newValue) => {
        setValue(newValue);
    }

    const fetchPatchListFromTournament = async (tournament) => {
        
        const header = {
            Authorization: "Bearer " + authTokens.access
        }
        const result = await fetch(API_URL + `dataAnalysis/patch/getFromTournament/${tournament}/`, {
            method: "GET",
            headers:header
        })
        result.json().then(result => {
            const newPatchList = result;
            setPatchList(newPatchList)
        })
    }

    

    useEffect(() => {
        

        const fetchTournamentList = async () => {
            const header = {
                Authorization: "Bearer " + authTokens.access
            }
            const result = await fetch(API_URL + "dataAnalysis/tournament/getList", {
                method: "GET",
                headers: header
            })
            result.json().then(result => {
                const newTournamentList = result.sort();
                setTournamentList(newTournamentList)
            })
        }
        
        fetchTournamentList();
    }, [])

    return(
        <div className="wrapper-champOverview">

            <NavBarComp/>
            <h1> Champion overview </h1>

            <div className="dashboard-champOverview-controlPannel">
                <ul className="dashboard-champOverview-controlPannel-list">
                    <li>
                        <SearchComp
                            defaultValue={activeTournament}
                            setSelectedElement={setActiveTournament}
                            elementList={tournamentList}
                            label={"Tournament"}
                            width={550}
                        />
                        
                    </li>
                    <li>
                        <SelectComp
                            elementList={side}
                            defaultValue={activeSide}
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