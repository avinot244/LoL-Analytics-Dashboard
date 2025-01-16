import { Typography, Stack, Button } from "@mui/material"
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import SearchIcon from '@mui/icons-material/Search';
import RestartAltIcon from '@mui/icons-material/RestartAlt';

import { useState, useEffect, useContext } from "react"

import NavBarComp from "../utils/NavbarComp"
import SearchComp from "../utils/SearchComp"
import { API_URL } from "../../constants"
import AuthContext from "../context/AuthContext"
import MultipleSearchComp from "../utils/MultipleSearchComp";

import "../../styles/TeamAnalysisOverall.css"

function TeamAnalysisOverall() {
    let {authTokens} = useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }
    const [activeTeam, setActiveTeam] = useState("")
    const [teamList, setTeamList] = useState([])

    const [displayTournamentSelecter, setDisplayTournamentSelecter] = useState(false)
    const [tournamentList, setTournamentList] = useState([])
    const [tournamentFilters, setTournamentFilters] = useState([])

    const [displayData, setDisplayData] = useState(false)


    const fetchTeamList = async () => {
        const result = await fetch(API_URL + `teamAnalysis/getAllTeams/`, {
            method: "GET",
            headers: header
        })
        result.json().then(data => {
            let newTeamList = data
            setTeamList(newTeamList)
        })
    }

    const fetchTournamentFromTeam = async (team) => {
        const result = await fetch(API_URL + `teamAnalysis/getTournamentsFromTeam/${team}/`, {
            method: "GET",
            headers: header
        })
        result.json().then(data => {
            let newTournamentList = data
            setTournamentList(newTournamentList)
            setDisplayTournamentSelecter(true)
        })
    }
    
    const handleAnalyze = (team, tournamentList) => {
        setDisplayData(true)
        console.log(team)
        console.log(tournamentList)
    }

    useEffect(() => {
        fetchTeamList()
    }, [])
    return (
        <div className="wrapper-teamAnalysisOverall">
            <NavBarComp />
            <Typography id="teamAnalysisOverall-title" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold", mb: 10}}>
                Team Analysis Overall
            </Typography>
            <Stack 
                direction={"row"}
                spacing={5}
                alignItems={"center"}
                justifySelf={"center"}
            >
                <SearchComp
                    defaultValue={activeTeam}
                    elementList={teamList}
                    setSelectedElement={setActiveTeam}
                    label={"Team"}
                    width={120}
                />

                <Button
                    variant="contained"
                    endIcon={<SearchIcon/>}
                    onClick={() => {
                        fetchTournamentFromTeam(activeTeam)
                    }}
                >
                    Search Tournament
                </Button>

                {
                    displayTournamentSelecter &&
                    <>
                        <MultipleSearchComp
                            tournamentFilterList={tournamentList}
                            selectedFilters={tournamentFilters}
                            setSelectedFilters={setTournamentFilters}
                            width={500}
                        />
                        <Button
                            variant="contained"
                            endIcon={<ArrowForwardIosIcon/>}
                            onClick={() => {
                                handleAnalyze(activeTeam, tournamentFilters)
                            }}
                        >
                            Analyze
                        </Button>
                        <Button
                            variant="contained"
                            endIcon={<RestartAltIcon/>}
                            onClick={() => {
                                setDisplayTournamentSelecter(false)
                                setDisplayData(false)
                            }}
                        >
                            Reset
                        </Button>
                    </>
                }
            </Stack>
            {
                displayData && 
                <>
                    <span>prout</span>
                </>
            }
            
        </div>
    )
}

export default TeamAnalysisOverall