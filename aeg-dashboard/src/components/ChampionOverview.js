import NavBarComp from "./NavbarComp";
import ChampionOverviewPanel from "./ChampionOverviewPanel"
import "../styles/ChampionOverview.css"
import SelectComp from "./SelectComp";

import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';

import { amber,  brown,  grey} from '@mui/material/colors/'

import { useState, useEffect } from "react";
import { ThemeProvider, createTheme } from "@mui/material";

import { API_URL } from "../constants";

import Button from "@mui/material/Button"
import SearchIcon from '@mui/icons-material/Search';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';

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

    const [activeData, setData] = useState([])

    const [activePatch, setActivePatch] = useState('Select a patch')
    const [activeSide, setActiveSide] = useState('Select a side')
    const [activeTournament, setActiveTournament] = useState("Select a tournament")

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

    const fetchChampionsDraftStats = async (tournament, patch, side) => {
        const result = await fetch(API_URL + `draft/championStats/getStats/${patch}/${side}/${tournament}/`, {
            method: "GET"
        })
        result.json().then(result => {
            const newData = result;
            setData(newData)
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
                const newTournamentList = result;
                setTournamentList(newTournamentList)
            })
        }
        


        fetchPatchList();
        fetchTournamentList();
    }, [])

    return(
        <div className="wrapper-overview">
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
                            }}    
                        >
                            Search Patches
                        </Button>
                    </li>
                </ul>
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
                                fetchChampionsDraftStats(activeTournament, activePatch, activeSide)
                            }}    
                        >
                            Analyze
                        </Button>
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
        
            
            <ChampionOverviewPanel value={value} panelIndex={0} data={activeData}/>
            <ChampionOverviewPanel value={value} panelIndex={1} data={activeData}/>
            <ChampionOverviewPanel value={value} panelIndex={2} data={activeData}/>
            <ChampionOverviewPanel value={value} panelIndex={3} data={activeData}/>
            <ChampionOverviewPanel value={value} panelIndex={4} data={activeData}/>
            <ChampionOverviewPanel value={value} panelIndex={5} data={activeData}/>
        </div>
    )
}


export default ChampionOverview