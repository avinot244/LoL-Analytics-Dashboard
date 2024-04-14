import NavBarComp from "./NavbarComp"
import "../styles/PlayerOverview.css"
import SelectComp from "./SelectComp";
import { useState, useEffect } from "react";
import ChampionIcon from "./ChampionIcon";
import { API_URL, roleList} from "../constants";

import Button from "@mui/material/Button"
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import SearchIcon from '@mui/icons-material/Search';
import RestartAltIcon from '@mui/icons-material/RestartAlt';

function PlayerOverview(){
    const [patchList, setPatchList] = useState([]);
    
    const weekList = ["Week 1", "Week 2", "Week 3"]

    const championList = ["Hwei", "Thresh", "Leona", "Maokai", "Senna", "Nautilus"]

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

    const gd15 = 450
    const k15 = 4
    const d15 = 1
    const a15 = 5

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
            const newPlayerList = result;
            setPlayerList(newPlayerList)
        })
    }

    const fetchTournamentFromPlayer = async (summonnerName) => {
        const result = await fetch(API_URL + `dataAnalysis/tournament/${summonnerName}/`, {
            metho: "GET"
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
                                    fetchTournamentFromPlayer(selectedPlayer)
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
                                    console.log(`Getting behavior analysis of player ${selectedPlayer} during tournament ${tournament} during patch ${activePatch} vs performance during latest ${activeLimit} games`)
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
                <div className="playerOverview-content-wrapper">
                    <div className="playerOverview-graph">
                    </div>
                    <div className="playerOverview-other-content">
                        <div className="playerOverview-stats">
                            <h2>Overall stats</h2>
                            <div className="playerOverview-stats-GD">
                                <p>
                                    AVG GD@15 : {gd15 > 0 ? `+${gd15} golds` : `-${gd15} golds`}
                                </p>
                            </div>
                            <div className="playerOverview-stats-kda">
                                <p>
                                    AVG K/D/A@15 : {`${k15}/${d15}/${a15}`}
                                </p>
                            </div>  
                        </div>
                        <br/>
                        <div className="playerOverview-champs">
                            <h2>Best champs</h2>
                            <ul className="playerOverview-champion-list">
                                {championList.map((championName) => 
                                    <ChampionIcon
                                        championName={championName}
                                        winRate={50}
                                        pickRate={60}
                                        banRate={30}
                                        pickOrder={1}
                                    />
                                )}
                            </ul>
                        </div>
                    </div>
                </div>
            }
            
        </div>
    )
}

export default PlayerOverview