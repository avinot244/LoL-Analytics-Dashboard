import NavBarComp from "../utils/NavbarComp"
import "../../styles/PlayerOverview.css"
import { useState, useEffect } from "react";
import PlayerOverviewStat from "./PlayerOverviewStat";
import { API_URL, roleList} from "../../constants";
import { ThemeProvider, createTheme, Typography } from "@mui/material";
import { TextField } from "@mui/material";
import Button from "@mui/material/Button"
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import SearchIcon from '@mui/icons-material/Search';
import Divider from "@mui/material/Divider";
import RestartAltIcon from '@mui/icons-material/RestartAlt';

import SearchComp from "../utils/SearchComp";
import AuthContext from "../context/AuthContext";
import PlayerOverviewChampPool from "./PlayerOverviewChampPool";

import { useContext } from "react";
//
function PlayerOverviewScrim(){
    const [patchList, setPatchList] = useState([]);
    
    const tournament = "League of Legends Scrims"

    const [activePatch, setActivePatch] = useState('')
    const [selectedPlayer, setSelectedPlayer] = useState('')
    const [activeRole, setActiveRole] = useState('')
    const [playerList, setPlayerList] = useState([])
    const [flagDisplayPlayerSearch, setDisplayPlayerSearch] = useState(false)
    const [flagDisplayPlayerStat, setDisplayPlayerStat] = useState(false)

    
    const [activeLimit, setActiveLimit] = useState(5)

    let {authTokens} = useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }

    const fetchPlayers = async (patch, role) => {
        const result = await fetch(API_URL + `behavior/${role}/getSummonnerListTournament/${patch}/${tournament}/`, {
            method: "GET",
            headers:header
        })
        result.json().then(result => {
            const newPlayerList = result.sort();
            setPlayerList(newPlayerList)
        })
    }

    const fetchPatchListFromScrim = async () => {
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
        fetchPatchListFromScrim();
    }, [])

    const theme = createTheme ({
        palette: {
            primary : {
                main: '#fff',
            },
            text : {
                disabled: '#fff'
            }
            
        },
        action: {
            active: '#fff'
        }
        
    })
    
    

    return(
        
        <div className="wrapper-overview-player">
            <NavBarComp/>
            <Typography id="PCAdocumentation-title" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold", mb: 10}}>
                Player Overview
            </Typography>
            <div className="dashboard-playerOverview-controlPannel">
                <ul className="dashboard-playerOverview-controlPannel-list">
                    <li>
                        <SearchComp
                            elementList={patchList}
                            defaultValue={"-- Patch --"}
                            setActive={setActivePatch}
                            width={160}
                        />
                    </li>
                    <li>
                        <SearchComp
                            elementList={roleList}
                            defaultValue={"-- Role --"}
                            setActive={setActiveRole}
                            width={160}
                        />
                    </li>
                    <li>
                        <Button
                            variant="contained"
                            endIcon={<SearchIcon />}
                            onClick={() => {
                                if (activePatch !== '' && activeRole !== '') {
                                    fetchPlayers(activePatch, activeRole)
                                    setDisplayPlayerSearch(true)
                                }
                            }}
                        >
                            Search
                        </Button>
                    </li>
                </ul>
            </div>
            {
                flagDisplayPlayerSearch && 
                <div className="playerOverview-playerSelect">
                    <ul className="dashboard-playerOverview-playerSelect-list">
                        <li>
                            <SearchComp
                                setSelectedElement={setSelectedPlayer}
                                elementList={playerList}
                                label={"Player"}
                                width={175}
                            />
                        </li>

                        <li>
                            <ThemeProvider theme={theme}>
                                <TextField
                                    id="outlined-number"
                                    label="Games"
                                    type="number"
                                    InputLabelProps={{
                                        shrink: true,
                                    }}
                                    sx={{ 
                                        input: { color: 'white'},
                                        borderColor: 'white'
                                    }}
                                    focused
                                    onChange={(e) => {
                                        setActiveLimit(e.target.value)
                                    }}
                                />
                            </ThemeProvider>
                        </li>

                        <li>
                            <Button 
                                variant="contained" 
                                endIcon={<RestartAltIcon />}
                                onClick={() => {
                                    setDisplayPlayerSearch(false)
                                    setDisplayPlayerStat(false)
                                }}    
                            >
                                Reset
                            </Button>
                        </li>
                        <li>
                            <Button
                                variant="contained"
                                endIcon={<ArrowForwardIosIcon/>}
                                onClick={() => {
                                    if (activePatch !== '' && activeRole !== '' && selectedPlayer !== '' && activeLimit > 0) {
                                        setDisplayPlayerStat(true)   
                                    }
                                }}
                            >
                                Analyse
                            </Button>
                        </li>                     
                    </ul>
                </div>
            }
            
            

            {
                flagDisplayPlayerStat && 
                <>
                    <PlayerOverviewStat 
                        role={activeRole}
                        summonnerName={selectedPlayer}
                        patch={activePatch}
                        wantedTournament={tournament}
                        limit={activeLimit}
                    />

                    <br />

                    <Divider
                        style={{ background: 'white', borderWidth: 1}}
                        variant="middle"
                    />   

                    <PlayerOverviewChampPool
                        summonnerName={selectedPlayer}
                        tournament={tournament}
                    />
                </>
                
            }
        </div>
    )
}

export default PlayerOverviewScrim