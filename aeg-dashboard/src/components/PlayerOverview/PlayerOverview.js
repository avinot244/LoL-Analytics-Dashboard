import Button from "@mui/material/Button"
import { Stack, TextField } from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material";
import Divider from "@mui/material/Divider";

import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import SearchIcon from '@mui/icons-material/Search';
import RestartAltIcon from '@mui/icons-material/RestartAlt';


import { useState, useEffect } from "react";
import { useContext } from "react";


import AuthContext from "../context/AuthContext";
import NavBarComp from "../utils/NavbarComp"
import SelectComp from "../utils/SelectComp";
import SearchComp from "../utils/SearchComp";
import PlayerOverviewStat from "./PlayerOverviewStat";
import PlayerOverviewChampPool from "./PlayerOverviewChampPool";
import { API_URL, roleList} from "../../constants";
import "../../styles/PlayerOverview.css"

function PlayerOverview({loggedIn, setLoggedIn}){
    const [patchList, setPatchList] = useState([]);
    

    
    const [activePatch1, setActivePatch1] = useState('')
    const [selectedPlayer1, setSelectedPlayer1] = useState('')
    const [activeRole1, setActiveRole1] = useState('')
    const [playerList1, setPlayerList1] = useState([])
    const [flagDisplayPlayerSearch1, setDisplayPlayerSearch1] = useState(false)
    const [flagDisplayPlayerStat1, setDisplayPlayerStat1] = useState(false)
    const [flagDisplayTournamentSearch1, setDisplayTournamentSearch1] = useState(false)
    const [tournament1, setActiveTournament1] = useState('')
    const [activeLimit1, setActiveLimit1] = useState(5)
    const [tournamentList1, setTournamentList1] = useState([])

    const [activePatch2, setActivePatch2] = useState('')
    const [selectedPlayer2, setSelectedPlayer2] = useState('')
    const [activeRole2, setActiveRole2] = useState('')
    const [playerList2, setPlayerList2] = useState([])
    const [flagDisplayPlayerSearch2, setDisplayPlayerSearch2] = useState(false)
    const [flagDisplayPlayerStat2, setDisplayPlayerStat2] = useState(false)
    const [flagDisplayTournamentSearch2, setDisplayTournamentSearch2] = useState(false)
    const [tournament2, setActiveTournament2] = useState('')
    const [activeLimit2, setActiveLimit2] = useState(5)
    const [tournamentList2, setTournamentList2] = useState([])

    
    

    let {authTokens} = useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }

    useEffect(() => {
        const fetchPatchList = async () => {
            const result = await fetch(API_URL + "dataAnalysis/patch/getList/0/", {
                method: "GET",
                headers:header
            })
            result.json().then(result => {
                const newPatchList = result;
                setPatchList(newPatchList);
            })
        }
        fetchPatchList();
    }, [])

    const fetchPlayers = async (patch, role, idx) => {
        const result = await fetch(API_URL + `behavior/${role}/getSummonnerList/${patch}/0/`, {
            method: "GET",
            headers:header
        })
        result.json().then(result => {
            const newPlayerList = result.sort();
            if (idx === 1){
                setPlayerList1(newPlayerList)
            } else if (idx === 2) {
                setPlayerList2(newPlayerList)
            }
        })
    }

    const fetchTournamentFromPlayer = async (summonnerName, patch, idx) => {
        const result = await fetch(API_URL + `dataAnalysis/tournament/${summonnerName}/${patch}/0/`, {
            method: "GET",
            headers:header
        })
        result.json().then(result => {
            const newTournamentListPlayer = result
            if (idx === 1) {
                setTournamentList1(newTournamentListPlayer)
            } else if (idx === 2) {
                setTournamentList2(newTournamentListPlayer)
            }
            
        })
    }


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
            <NavBarComp loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>
            <h1> Player Overview </h1>
            <Stack spacing={2} direction="row" justifyContent="center" alignItems="center">
                <div className="dashboard-playerOverview-controlPannel-wrapper">
                    <div className="dashboard-playerOverview-controlPannel">
                        <ul className="dashboard-playerOverview-controlPannel-list">
                            <li>
                                <SelectComp
                                    elementList={patchList}
                                    defaultValue={"-- Patch --"}
                                    setActive={setActivePatch1}/>
                            </li>
                            <li>
                                <SelectComp
                                    elementList={roleList}
                                    defaultValue={"-- Role --"}
                                    setActive={setActiveRole1}/>
                            </li>
                            <li>
                                <Button
                                    variant="contained"
                                    endIcon={<SearchIcon />}
                                    onClick={() => {
                                        console.log(activePatch1, activeRole1)
                                        if (activePatch1 !== '' && activeRole1 !== '') {
                                            fetchPlayers(activePatch1, activeRole1, 1)
                                            setDisplayPlayerSearch1(true)
                                        }
                                    }}
                                >
                                    Search
                                </Button>
                            </li>
                        </ul>
                    </div>

                    {
                        flagDisplayPlayerSearch1 && 
                        <div className="playerOverview-playerSelect">
                            <ul className="dashboard-playerOverview-playerSelect-list">
                                <li>
                                    <SearchComp
                                        setSelectedElement={setSelectedPlayer1}
                                        elementList={playerList1}
                                        label={"Player"}
                                        width={175}
                                    />
                                </li>

                                <li>
                                    <Button 
                                        variant="contained" 
                                        endIcon={<SearchIcon />}
                                        onClick={() => {
                                            if (selectedPlayer1 !== '') {
                                                setDisplayTournamentSearch1(true)
                                                fetchTournamentFromPlayer(selectedPlayer1, activePatch1, 1)
                                            }
                                        }}    
                                    >
                                        Search tournament
                                    </Button>
                                </li>

                                
                            </ul>
                        </div>
                    }
                    
                    {
                        flagDisplayTournamentSearch1 &&
                        <div className="playerOverview-searchTournament">
                            <ul className="dashboard-playerOverview-searchTournament-list">
                                <li>
                                    <SelectComp 
                                        elementList={tournamentList1}
                                        defaultValue={"-- Tournament --"}
                                        setActive={setActiveTournament1}
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
                                                setActiveLimit1(e.target.value)
                                            }}
                                        />
                                    </ThemeProvider>
                                </li>

                                <li>
                                    <Button 
                                        variant="contained" 
                                        endIcon={<RestartAltIcon />}
                                        onClick={() => {
                                            setDisplayPlayerSearch1(false)
                                            setDisplayPlayerStat1(false)
                                            setDisplayTournamentSearch1(false)
                                            setActiveLimit1(5)
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
                                            if (tournament1 !== '' && activeLimit1 > 0) {
                                                setDisplayPlayerStat1(true)
                                            }
                                        }}
                                    >
                                        Analyse
                                    </Button>
                                </li>
                            </ul>
                        </div>
                    }
                </div>

                <div className="dashboard-playerOverview-controlPannel-wrapper">
                    <div className="dashboard-playerOverview-controlPannel">
                        <ul className="dashboard-playerOverview-controlPannel-list">
                            <li>
                                <SelectComp
                                    elementList={patchList}
                                    defaultValue={"-- Patch --"}
                                    setActive={setActivePatch2}/>
                            </li>
                            <li>
                                <SelectComp
                                    elementList={roleList}
                                    defaultValue={"-- Role --"}
                                    setActive={setActiveRole2}/>
                            </li>
                            <li>
                                <Button
                                    variant="contained"
                                    endIcon={<SearchIcon />}
                                    onClick={() => {
                                        console.log(activePatch2, activeRole2)
                                        if (activePatch2 !== '' && activeRole2 !== '') {
                                            fetchPlayers(activePatch2, activeRole2, 2)
                                            setDisplayPlayerSearch2(true)
                                        }
                                    }}
                                >
                                    Search
                                </Button>
                            </li>
                        </ul>
                    </div>

                    {
                        flagDisplayPlayerSearch2 && 
                        <div className="playerOverview-playerSelect">
                            <ul className="dashboard-playerOverview-playerSelect-list">
                                <li>
                                    <SearchComp
                                        setSelectedElement={setSelectedPlayer2}
                                        elementList={playerList2}
                                        label={"Player"}
                                        width={175}
                                    />
                                </li>

                                <li>
                                    <Button 
                                        variant="contained" 
                                        endIcon={<SearchIcon />}
                                        onClick={() => {
                                            if (selectedPlayer2 !== '') {
                                                setDisplayTournamentSearch2(true)
                                                fetchTournamentFromPlayer(selectedPlayer2, activePatch2, 2)
                                            }
                                        }}    
                                    >
                                        Search tournament
                                    </Button>
                                </li>

                                
                            </ul>
                        </div>
                    }
                    
                    {
                        flagDisplayTournamentSearch2 &&
                        <div className="playerOverview-searchTournament">
                            <ul className="dashboard-playerOverview-searchTournament-list">
                                <li>
                                    <SelectComp 
                                        elementList={tournamentList2}
                                        defaultValue={"-- Tournament --"}
                                        setActive={setActiveTournament2}
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
                                                setActiveLimit2(e.target.value)
                                            }}
                                        />
                                    </ThemeProvider>
                                </li>

                                <li>
                                    <Button 
                                        variant="contained" 
                                        endIcon={<RestartAltIcon />}
                                        onClick={() => {
                                            setDisplayPlayerSearch2(false)
                                            setDisplayPlayerStat2(false)
                                            setDisplayTournamentSearch2(false)
                                            setActiveLimit2(5)
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
                                            if (tournament2 !== '' && activeLimit2 > 0) {
                                                setDisplayPlayerStat2(true)
                                            }
                                        }}
                                    >
                                        Analyse
                                    </Button>
                                </li>
                            </ul>
                        </div>
                    }
                </div>
            </Stack>
            

            <Stack spacing={5} direction="row" justifyContent="center" alignItems="center">
                {
                    flagDisplayPlayerStat1 ? ( 
                        <Stack spacing={1} direction="column" justifyContent="center" alignItems="center">
                            <PlayerOverviewStat 
                                role={activeRole1}
                                summonnerName={selectedPlayer1}
                                patch={activePatch1}
                                wantedTournament={tournament1}
                                limit={activeLimit1}
                            />
                            <br />

                            <Divider
                                style={{ background: 'white', borderWidth: 1}}
                                variant="middle"
                            />   

                            <PlayerOverviewChampPool
                                summonnerName={selectedPlayer1}
                                tournament={tournament1}
                            />
                        </Stack>
                    ) : (
                        <div className="playerOverview-placeholder"></div>
                    )
                }

                {
                    
                    flagDisplayPlayerStat2 ? (
                        <Stack spacing={1} direction="column" justifyContent="center" alignItems="center">
                            <PlayerOverviewStat 
                                role={activeRole2}
                                summonnerName={selectedPlayer2}
                                patch={activePatch2}
                                wantedTournament={tournament2}
                                limit={activeLimit2}
                            />

                            <br />

                            <Divider
                                style={{ background: 'white', borderWidth: 1}}
                                variant="middle"
                            />   

                            <PlayerOverviewChampPool
                                summonnerName={selectedPlayer2}
                                tournament={tournament2}
                            />
                        </Stack>
                    ) : (
                        <div className="playerOverview-placeholder"></div>
                    )
                }
                
                
            </Stack>
                    

                    
        </div>
    )
}

export default PlayerOverview