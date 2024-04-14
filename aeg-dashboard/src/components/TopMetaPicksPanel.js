import SelectComp from "./SelectComp";
import { useState, useEffect } from "react";
import { API_URL } from "../constants";
import ChampionOverviewListPanel from "./championOverviewListPanel";

import Button from "@mui/material/Button"
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import SearchIcon from '@mui/icons-material/Search';
import RestartAltIcon from '@mui/icons-material/RestartAlt';


function TopMetaPicksPanel(props) {
    const [patchList, setPatchList] = useState([]);
    
    const [activePatch, setActivePatch] = useState()
    const [activeSide, setActiveSide] = useState()
    const [activeTournament, setActiveTournament] = useState()
    const [activeFilter, setActiveFilter] = useState()

    const [flagChampionOverview, setFlagChampionOverview] = useState(false)

    const {value, panelIndex} = props
    const side = ["Blue", "Red", "Both"];
    const [tournamentList, setTournamentList] = useState([])
    const [displayPatchFlag, setDisplayPatchFlag] = useState(false)
    const filterList = ["WinRate", "PickRate", "BanRate", "PickOrder"]


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
        const fetchTournamentList = async () => {
            const result = await fetch(API_URL + "dataAnalysis/tournament/getList", {
                method: "GET"
            })
            result.json().then(result => {
                const newTournamentList = result;
                setTournamentList(newTournamentList)
                setActiveTournament(newTournamentList[newTournamentList.length - 1])
            })
        }
        
        fetchTournamentList();
        setActiveSide("Blue")
        setActiveFilter(filterList[0])
        
    }, [])
    
    return (
        <div
            role='tabpanbel'
            hidden={value !== panelIndex}
            className={`simple-tabpanel-${panelIndex}`}
            aria-labelledby={`simple-tab-${panelIndex}`}
        >
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
            </div>

            {
                displayPatchFlag &&

                <div className="sorter">
                    <ul>
                        <li>
                            <li>
                                <SelectComp 
                                    elementList={patchList}
                                    defaultValue={"-- Patch --"}
                                    setActive={setActivePatch}
                                />
                            </li>
                        </li>
                        <li>Sort by</li>
                        <li>
                            <SelectComp 
                                elementList={filterList}
                                defaultValue={"-- Select Filter --"}
                                setActive={setActiveFilter}
                            />
                        </li>
                        <li>
                            <Button 
                                variant="contained" 
                                endIcon={<ArrowForwardIosIcon />}
                                onClick={() => {
                                    setFlagChampionOverview(true)
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
                                    setDisplayPatchFlag(false)
                                    setFlagChampionOverview(false)
                                }}    
                            >
                                Reset
                            </Button>
                        </li>
                    </ul>                
                </div>
            }
            
            {
                flagChampionOverview &&
                <ChampionOverviewListPanel
                    filter={activeFilter}
                    side={activeSide}
                    patch={activePatch}
                    tournament={activeTournament}
                />
            }
            
        </div>
    )
}

export default TopMetaPicksPanel;