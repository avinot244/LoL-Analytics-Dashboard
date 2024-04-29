import NavBarComp from "../NavbarComp"
import "../../styles/GameOverview.css"
import SearchComp from "../SearchComp"
import { API_URL } from "../../constants"

import Stack from '@mui/material/Stack'
import Button from "@mui/material/Button"
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import SearchIcon from '@mui/icons-material/Search';
import RestartAltIcon from '@mui/icons-material/RestartAlt';

import { useState, useEffect } from "react"


function GameOverview(){

    const [gameList, setGameList] = useState([])
    const [selectedGame, setSelectedGame] = useState('')


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
            console.log(result)
            const newGameList = result.sort()
            setGameList(newGameList)
            setSelectedGame(newGameList[newGameList.length - 1])
        })
    }

    return(
        <div className="wrapper-overview-game">
            <NavBarComp />
            <h1> Game overview </h1>
            <br/>
            <Stack spacing={2} direction="row" justifyContent="center">
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
                <Stack spacing={2} direction="row" justifyContent="center">
                    <SearchComp 
                        label={"Games"}
                        elementList={gameList}
                        setSelectedElement={setSelectedGame}
                        width={275}
                    />
                    <Button 
                        variant="contained" 
                        endIcon={<ArrowForwardIosIcon />}>
                    
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
            
            <p>{selectedGame}</p>
        </div>
        
    )
}

export default GameOverview