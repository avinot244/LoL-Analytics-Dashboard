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
import TeamAnalysisDetailsData from "./TeamAnalysisDetailsData";


import "../../styles/TeamAnalysisDetails.css"

function SearchGameComp({setSelectedElement, elementList, label, width, multiple, defaultValue}) {
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
    
    const handleChange = (value) => {
		if (value != null) {
			setSelectedElement(value)
		}
	}
	return (	
		<>
			<ThemeProvider theme={theme}>
				<Box sx={{ color: 'primary.main' , borderColor: 'white'}}>
					<Autocomplete
						defaultValue={defaultValue}
						multiple={multiple}
						clearIcon={<ClearIcon color="error"/>}
						popupIcon={<ArrowDropDownIcon color="primary"/>}
						className="searchComp"
						options={elementList}
                        getOptionLabel={option => option.str}
						renderInput={(params) => (
							<TextField 
								className='textField-searchComp'
								{...params} 
								label={label}
								sx={{ 
									input: { color: 'white'},
									borderColor: 'white'
								}}
								focused
								fullWidth={true}
							/>
							
						)}
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
    const [selectedGame, setSelectedGame] = useState("")

    const [displayData, setDisplayData] = useState(false)



    const fetchTeamList = async () => {
        const result = await fetch(API_URL + `teamAnalysis/getAllTeams/`, {
            method: "GET",
            headers: header
        })
        result.json().then(data => {
            let newTeamList = data
            newTeamList.sort()
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
            const newGameList = data
            setGameList(newGameList)
        })
    }

    
    
    const handleAnalyze = () => {
        setDisplayData(true)
        console.log(selectedGame)
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
                    <SearchGameComp
                        elementList={gameList}
                        setSelectedElement={setSelectedGame}
                        label={"Game"}
                        width={550}
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
            <br/>
            <br/>
            {
                displayData && (
                    <TeamAnalysisDetailsData 
                        seriesId={selectedGame.seriesId} 
                        gameNumber={selectedGame.gameNumber}
                        team={activeTeam}
                    />
                )
            }
            
        </div>
    )
}

export default TeamAnalysisDetails