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
import SearchComp from "../SearchComp";

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

    

    const fetchPlayers = async (patch, role) => {
        const result = await fetch(API_URL + `behavior/${role}/getSummonnerListTournament/${patch}/${tournament}/`, {
            method: "GET"
        })
        result.json().then(result => {
            const newPlayerList = result.sort();
            setPlayerList(newPlayerList)
        })
    }

    const fetchPatchListFromScrim = async () => {
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
        fetchPatchListFromScrim();
    }, [])

    
    

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
                                if (activePatch != '' && activeRole != '') {
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
                                    if (activePatch != '' && activeRole != '' && selectedPlayer != '') {
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
            
        </div>
    )
}

export default PlayerOverviewScrim