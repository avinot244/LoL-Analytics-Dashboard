import SelectComp from "../utils/SelectComp";
import { useState, useEffect, useContext } from "react";
import { API_URL } from "../../constants";
import ChampionOverviewListPanel from "../ChampionOverview/championOverviewListPanel";

import Button from "@mui/material/Button"
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import SearchIcon from '@mui/icons-material/Search';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import SearchComp from "../utils/SearchComp";
import AuthContext from "../context/AuthContext";


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
    const filterList = ["WinRate", "PickRate", "BanRate"]

    let {authTokens} = useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }

    const fetchPatchListFromTournament = async (tournament) => {
        const result = await fetch(API_URL + `dataAnalysis/patch/getFromTournament/${tournament}/`, {
            method: "GET",
            headers: header
        })
        result.json().then(result => {
            const newPatchList = result;
            setPatchList(newPatchList)
            const latestPatch = newPatchList[newPatchList.length - 1]
            setActivePatch(latestPatch)
        })
    }


    useEffect(() => {
        const fetchTournamentList = async () => {
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
                        <SearchComp
                            defaultValue={activeTournament}
                            elementList={tournamentList}
                            setSelectedElement={setActiveTournament}
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
            </div>

            {
                displayPatchFlag &&

                <div className="sorter">
                    <ul>
                        <li>
                            <li>
                                <SelectComp
                                    elementList={patchList}
                                    defaultValue={activePatch}
                                    setActive={setActivePatch}
                                />
                            </li>
                        </li>
                        <li>Sort by</li>
                        <li>
                            <SelectComp 
                                elementList={filterList}
                                defaultValue={activeFilter}
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