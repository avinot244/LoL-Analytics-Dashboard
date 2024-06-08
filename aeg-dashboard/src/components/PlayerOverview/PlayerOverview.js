import NavBarComp from "../NavbarComp"
import "../../styles/PlayerOverview.css"
import SelectComp from "../SelectComp";
import { useState, useEffect } from "react";
import PlayerOverviewStat from "./PlayerOverviewStat";
import { API_URL, roleList} from "../../constants";

import Button from "@mui/material/Button"
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import SearchIcon from '@mui/icons-material/Search';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import SearchComp from "../SearchComp";
import { TextField } from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material";
import RedirectPage from "../Home/RedirectPage";

function PlayerOverview({loggedIn, setLoggedIn}){
    const [patchList, setPatchList] = useState([]);
    
    const [activePatch, setActivePatch] = useState('')
    const [selectedPlayer, setSelectedPlayer] = useState('')
    const [activeRole, setActiveRole] = useState('')
    const [playerList, setPlayerList] = useState([])
    const [flagDisplayPlayerSearch, setDisplayPlayerSearch] = useState(false)
    const [flagDisplayPlayerStat, setDisplayPlayerStat] = useState(false)
    const [flagDisplayTournamentSearch, setDisplayTournamentSearch] = useState(false)

    const [tournamentList, setTournamentList] = useState([])
    const [tournament, setActiveTournament] = useState('')
    const [activeLimit, setActiveLimit] = useState(5)

    useEffect(() => {
        const fetchPatchList = async () => {
            const result = await fetch(API_URL + "dataAnalysis/patch/getList/0/", {
                method: "GET"
            })
            result.json().then(result => {
                const newPatchList = result;
                setPatchList(newPatchList);
            })
        }
        fetchPatchList();
    }, [])

    const fetchPlayers = async (patch, role) => {
        const result = await fetch(API_URL + `behavior/${role}/getSummonnerList/${patch}/0/`, {
            method: "GET"
        })
        result.json().then(result => {
            const newPlayerList = result.sort();
            setPlayerList(newPlayerList)
        })
    }

    const fetchTournamentFromPlayer = async (summonnerName, patch) => {
        const result = await fetch(API_URL + `dataAnalysis/tournament/${summonnerName}/${patch}/0/`, {
            method: "GET"
        })
        result.json().then(result => {
            const newTournamentListPlayer = result
            setTournamentList(newTournamentListPlayer)
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

            {
                loggedIn ? (
                    <>
                        <NavBarComp loggedIn={loggedIn} setLoggedIn={setLoggedIn}/>
                        <h1> Player Overview </h1>
                        <div className="dashboard-playerOverview-controlPannel">
                            <ul className="dashboard-playerOverview-controlPannel-list">
                                <li>
                                    <SelectComp
                                        elementList={patchList}
                                        defaultValue={"-- Patch --"}
                                        setActive={setActivePatch}/>
                                </li>
                                <li>
                                    <SelectComp
                                        elementList={roleList}
                                        defaultValue={"-- Role --"}
                                        setActive={setActiveRole}/>
                                </li>
                                <li>
                                    <Button
                                        variant="contained"
                                        endIcon={<SearchIcon />}
                                        onClick={() => {
                                            console.log(activePatch, activeRole)
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
                                        <Button 
                                            variant="contained" 
                                            endIcon={<SearchIcon />}
                                            onClick={() => {
                                                if (selectedPlayer !== '') {
                                                    setDisplayTournamentSearch(true)
                                                    fetchTournamentFromPlayer(selectedPlayer, activePatch)
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
                            flagDisplayTournamentSearch &&
                            <div className="playerOverview-searchTournament">
                                <ul className="dashboard-playerOverview-searchTournament-list">
                                    <li>
                                        <SelectComp 
                                            elementList={tournamentList}
                                            defaultValue={"-- Tournament --"}
                                            setActive={setActiveTournament}
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
                                                setDisplayTournamentSearch(false)
                                                setActiveLimit(5)
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
                                                if (tournament !== '' && activeLimit > 0) {
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
                            <PlayerOverviewStat 
                                role={activeRole}
                                summonnerName={selectedPlayer}
                                patch={activePatch}
                                wantedTournament={tournament}
                                limit={activeLimit}
                            />
                        }
                    </>
                ) : (
                    <RedirectPage />
                )

            }
            
            
        </div>
    )
}

export default PlayerOverview