import NavBarComp from "../NavbarComp"
import "../../styles/GameOverview.css"
import SearchComp from "../SearchComp"
import { API_URL } from "../../constants"

import { Chip, ThemeProvider, createTheme } from "@mui/material";
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

import { useState, useEffect, Fragment } from "react"

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
                        multiple
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
                        renderTags={(tagValue, getTagProps) => (
                            tagValue.map((option, index) => {
                                let label = `${option.seriesId} ${option.gameNumber}`
                                return (
                                    <Chip
                                        label={label}
                                        color="primary"
                                        variant="outlined"
                                        {...getTagProps({ index })}
                                    />
                                )
                            })
                        )}
					/>
				</Box>
				
			</ThemeProvider>
        </>
    )
}


function GameOverview(){

    const [gameList, setGameList] = useState([])
    const [selectedGames, setSelectedGame] = useState('')


    const [tournamentList, setTournamentList] = useState([])
    const [tournament, setActiveTournament] = useState('')

    const [flagGameSelecter, setFlagGameSelecter] = useState(false)
    

    useEffect(() => {
        const fetchTournamentList = async () => {
            const result = await fetch(API_URL + "dataAnalysis/tournament/getList", {
                method: "GET"
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
            method: "GET"
        })
        result.json().then(result => {
            // let newGameList = []
            // for (let i = 0 ; i < result.data.length ; i ++) {
            //     let gameObject = result.data[i]
            //     console.log(gameObject)
            //     newGameList.push(gameObject.str)

            // }
            // setGameList(newGameList.sort())
            const newGameList = result.data
            setGameList(newGameList)
            setSelectedGame(newGameList[newGameList.length - 1])
        })
    }

    const fetchPositionDensity = async (gameList) => {
        const result = await fetch(API_URL + "dataAnalysis/getGamePositionDensity/", {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify(gameList)
        })
        

    }

    const handleAnalyze = (gameList) => {
        if (gameList.length > 0) {
            fetchPositionDensity(gameList)
        }else{
            alert("Please select at least one game")
        }
    }
    

    return(
        <div className="wrapper-overview-game">
            <NavBarComp />
            <h1> Game overview </h1>
            <br/>
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
                            handleAnalyze(selectedGames)
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
                        }}
                    >
                        Reset
                    </Button>
                    
                </Stack>

            }
            
            {
                selectedGames.length > 0 &&
                selectedGames.map((object) => {
                    return (
                        <p>{object.seriesId} {object.gameNumber}</p>
                    )
                })

            }
        </div>
        
    )
}

export default GameOverview