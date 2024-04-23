import NavBarComp from "../NavbarComp"
import "../../styles/PlayerOverview.css"
import SelectComp from "../SelectComp";
import { useState, useEffect } from "react";
import PlayerOverviewStat from "./PlayerOverviewStat";
import { API_URL, roleList, behaviorModelUUID} from "../../constants";

import Button from "@mui/material/Button"
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import SearchIcon from '@mui/icons-material/Search';
import RestartAltIcon from '@mui/icons-material/RestartAlt';

function PlayerOverview(){
    const [patchList, setPatchList] = useState([]);
    
    const [activePatch, setActivePatch] = useState('Select a patch')
    const [selectedPlayer, setSelectedPlayer] = useState('Select a player')
    const [activeRole, setActiveRole] = useState('Select a role')
    const [playerList, setPlayerList] = useState([])
    const [flagDisplayPlayerSearch, setDisplayPlayerSearch] = useState(false)
    const [flagDisplayPlayerStat, setDisplayPlayerStat] = useState(false)
    const [flagDisplayTournamentSearch, setDisplayTournamentSearch] = useState(false)

    const [tournamentList, setTournamentList] = useState([])
    const [tournament, setActiveTournament] = useState([])
    const [activeLimit, setActiveLimit] = useState(5)

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
        fetchPatchList();
    }, [])

    const fetchPlayers = async (patch, role) => {
        const result = await fetch(API_URL + `behavior/${role}/getSummonnerList/${patch}/`, {
            method: "GET"
        })
        result.json().then(result => {
            const newPlayerList = result.sort();
            setPlayerList(newPlayerList)
        })
    }

    const fetchTournamentFromPlayer = async (summonnerName, patch) => {
        const result = await fetch(API_URL + `dataAnalysis/tournament/${summonnerName}/${patch}`, {
            method: "GET"
        })
        result.json().then(result => {
            const newTournamentListPlayer = result
            setTournamentList(newTournamentListPlayer)
        })
    }

    
    

    return(
        
        <div className="wrapper-overview-player">
            <NavBarComp />
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
                                fetchPlayers(activePatch, activeRole)
                                setDisplayPlayerSearch(true)
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
                            <SelectComp
                                elementList={playerList}
                                defaultValue={"-- Player --"}
                                setActive={setSelectedPlayer}
                            />
                        </li>

                        <li>
                            <Button 
                                variant="contained" 
                                endIcon={<SearchIcon />}
                                onClick={() => {
                                    setDisplayTournamentSearch(true)
                                    fetchTournamentFromPlayer(selectedPlayer, activePatch)
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
                            <SelectComp
                                elementList={[5, 10, 15]}
                                defaultValue={"-- Select a value --"}
                                setActive={setActiveLimit}
                            />
                        </li>

                        <li>
                            <Button 
                                variant="contained" 
                                endIcon={<RestartAltIcon />}
                                onClick={() => {
                                    setDisplayPlayerSearch(false)
                                    setDisplayPlayerStat(false)
                                    setDisplayTournamentSearch(false)
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
                                    setDisplayPlayerStat(true)
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
            
        </div>
    )
}

export default PlayerOverview