import { Typography, Stack, Button, Box, Autocomplete, Chip, ThemeProvider, createTheme, TextField } from "@mui/material"
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import SearchIcon from '@mui/icons-material/Search';
import ClearIcon from '@mui/icons-material/Clear'
import RestartAltIcon from '@mui/icons-material/RestartAlt';

import { useState, useEffect, useContext } from "react"

import NavBarComp from "../utils/NavbarComp"
import SearchComp from "../utils/SearchComp"
import { API_URL } from "../../constants"
import AuthContext from "../context/AuthContext"
import MultipleSearchComp from "../utils/MultipleSearchComp";



import "../../styles/TeamAnalysisDetails.css"


function MultipleGameSearch({tournamentFilterList, selectedFilters, setSelectedFilters, width}) {
    const handleChange = (list) => {
        const newFilters = list
        console.log(newFilters)
        setSelectedFilters(newFilters)
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

    return (
        <>	
            <ThemeProvider theme={theme}>
                <Box sx={{ color: 'primary.main' , borderColor: 'white'}}>
                    <Autocomplete
                        multiple
                        clearIcon={<ClearIcon color="error"/>}
                        popupIcon={<ArrowDropDownIcon color="primary"/>}
                        className="searchComp"
                        options={tournamentFilterList}
                        getOptionLabel={option => option.str}
                        renderInput={(params) => (
                            <TextField 
                                {...params} 
                                className='textField-searchComp'
                                label={"Tournament Filter"}
                                focused
                                sx={{ 
                                        input: { color: 'white'},
                                        borderColor: 'white'
                                    }}
                                
                            />
                        )}
                        renderTags={(value, getTagProps) => 
                            value.map((option, index) => (
                                <Chip
                                    color="primary"
                                    variant='outlined'
                                    label={option.str}
                                    {...getTagProps({index})}
                                />
                            ))
                        }
                        onChange={(_, value) => {handleChange(value)}}
                        sx={{color: 'primary.main', borderColor: 'primary.main', width: width}}
                        fullWidth={true}
                    />
                </Box>
                
            </ThemeProvider>
        </>
	);
}

function TeamAnalysisDetails() {
    let {authTokens} = useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }
    const [activeTeam, setActiveTeam] = useState("")
    const [teamList, setTeamList] = useState([])

    const [displayTournamentSelecter, setDisplayTournamentSelecter] = useState(false)
    const [tournamentList, setTournamentList] = useState([])
    const [tournamentFilters, setTournamentFilters] = useState([])

    const [displayGameSelecter, setDisplayGameSelecter] = useState(false)
    const [gameList, setGameList] = useState([])
    const [selectedGames, setSelectedGames] = useState([])

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

    const fetchGames = async (team, tournamentList) => {
        console.log(`fetching games for team ${team} in tournaments ${tournamentList}`)
        
        const data = {
            "team": team,
            "tournaments": tournamentList
        }

        const result = await fetch(API_URL + `teamAnalysis/getGames/`, {
            method: "PATCH",
            body: JSON.stringify(data),
            headers: header
        })

        result.json().then(data => {
            console.log(data)
            const newGameList = data
            setGameList(newGameList)
        })
    }
    
    const handleAnalyze = (team, tournamentList) => {
        setDisplayGameSelecter(true)
        console.log(team)
        console.log(tournamentList)
    }

    useEffect(() => {
        fetchTeamList()
    }, [])
    return (
        <div className="wrapper-teamAnalysisDetails">
            <NavBarComp />
            <Typography id="teamAnalysisDetails-title" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold", mb: 10}}>
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
                            endIcon={<SearchIcon/>}
                            onClick={() => {
                                setDisplayGameSelecter(true)
                                fetchGames(activeTeam, tournamentFilters)
                            }}
                        >
                            Get Games
                        </Button>
                        
                    </>
                }
                <Button
                    variant="contained"
                    endIcon={<RestartAltIcon/>}
                    onClick={() => {
                        setDisplayTournamentSelecter(false)
                        setDisplayGameSelecter(false)
                        setDisplayData(false)
                    }}
                >
                    Reset
                </Button>
            </Stack>
            {
                displayGameSelecter && 
                <Stack 
                    direction={"row"}
                    spacing={5}
                    alignItems={"center"}
                    justifySelf={"center"}
                    sx={{
                        pt:2
                    }}
                >
                    <MultipleGameSearch
                        tournamentFilterList={gameList}
                        selectedFilters={selectedGames}
                        setSelectedFilters={setSelectedGames}
                        width={500}
                    />
                    <Button
                        variant="contained"
                        endIcon={<ArrowForwardIosIcon/>}
                        onClick={() => {
                            handleAnalyze()
                        }}
                    >
                        Analyze
                    </Button>
                </Stack>
            }
            
            {
                displayData && 
                <>
                    <span>prout</span>
                </>
            }
            
        </div>
    )
}

export default TeamAnalysisDetails