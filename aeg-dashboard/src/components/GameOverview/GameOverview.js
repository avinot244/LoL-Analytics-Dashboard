import NavBarComp from "../utils/NavbarComp"
import "../../styles/GameOverview.css"
import SearchComp from "../utils/SearchComp"
import { API_URL } from "../../constants"
import GameOverviewStat from "./GameOverviewStat"
import MultipleSearchComp from "../utils/MultipleSearchComp"

import { ThemeProvider, createTheme, Typography } from "@mui/material";
import { Autocomplete } from '@mui/material';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack'
import Button from "@mui/material/Button"
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import SearchIcon from '@mui/icons-material/Search';
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import ClearIcon from '@mui/icons-material/Clear';

import { useState, useEffect, useContext } from "react"
import AuthContext from "../context/AuthContext"

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

function SearchGames({setSelectedElement, elementList}) {
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
						clearIcon={<ClearIcon color="error"/>}
						popupIcon={<ArrowDropDownIcon color="primary"/>}
						options={elementList}
                        getOptionLabel={option => option.str}
						renderInput={(params) => (
								<TextField 
									className='textField-searchComp'
									{...params} 
									label={"Games"}
									sx={{ 
										input: { color: 'white'},
										borderColor: 'white'
									}}
									focused

								/>
							
							)}
						onChange={(_, gameObject) => {handleChange(gameObject)}}
						sx={{color: 'primary.main', borderColor: 'primary.main', width: 425}}
                        
					/>
				</Box>
				
			</ThemeProvider>
        </>
    )
}


function GameOverview(){

    const [gameList, setGameList] = useState([])
    const [selectedGame, setSelectedGame] = useState('')


    const [tournamentList, setTournamentList] = useState([])
    const [tournament, setActiveTournament] = useState('')

    const [flagGameSelecter, setFlagGameSelecter] = useState(false)
    const [flagDisplayStat, setFlagDisplayState] = useState(false)

    let {authTokens} = useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
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
                setActiveTournament(newTournamentList[newTournamentList.length - 1])
            })
        }
        
        fetchTournamentList();
    }, [])

    const fetchGamesFromTournament = async () => {
        const result = await fetch(API_URL + `dataAnalysis/getGameList/${tournament}/`, {
            method: "GET",
            headers: header
        })
        result.json().then(result => {
            const newGameList = result.data
            setGameList(newGameList)
            setSelectedGame(newGameList[newGameList.length - 1])
        })
    }


    return(
        <div className="wrapper-overview-game">
            <NavBarComp/>
            <Typography id="PCAdocumentation-title" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold", mb: 10}}>
                Game Overview
            </Typography>
            <Stack spacing={2} direction="row" justifyContent="center" alignItems="center">
                <SearchComp
                    elementList={tournamentList}
                    setSelectedElement={setActiveTournament}
                    label={"Tournament"}
                    width={550}
                />

                <Button
                    variant="contained"
                    endIcon={<SearchIcon />}
                    onClick={() => {
                        fetchGamesFromTournament(tournament)
                        setFlagGameSelecter(true)
                    }}
                >
                    Search Games
                </Button>
            </Stack>
            
            <br/>


            {
                flagGameSelecter && 
                <Stack spacing={2} direction="row" justifyContent="center" alignItems="center">
                    <SearchGames
                        setSelectedElement={setSelectedGame}
                        elementList={gameList}
                    />
                    <Button 
                        variant="contained" 
                        endIcon={<ArrowForwardIosIcon />}         
                        onClick = {() => {
                            setFlagDisplayState(true)
                        }}               
                    >
                        Analyze
                    </Button>
                    <Button
                        variant="contained"
                        endIcon={<RestartAltIcon/>}
                        onClick={() => {
                            setFlagGameSelecter(false)
                            setSelectedGame('')
                            setFlagDisplayState(false)
                        }}
                    >
                        Reset
                    </Button>
                    
                </Stack>

            }
            
            
            {
                flagDisplayStat &&
                <GameOverviewStat 
                    seriesId={selectedGame.seriesId}
                    gameNumber={selectedGame.gameNumber}
                />
            }
        </div>
    )
}

export default GameOverview