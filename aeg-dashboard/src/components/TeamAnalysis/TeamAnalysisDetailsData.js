import { API_URL } from "../../constants";
import AuthContext from "../context/AuthContext";
import TeamAnalysisDetailsDataPosition from "./TeamAnalysisDetailsDataPosition";
import TeamAnalysisDetailsDataReset from "./TeamAnalysisDetailsDataReset";
import TeamAnalysisDetailsDataWard from "./TeamAnalysisDetailsDataWard";
import TeamAnalysisDetailsDataTP from "./TeamAnalysisDetailsDataTP";
import TimeFrameSelecter from "../utils/TimeFrameSelecter/TimeFrameSelecter";

import { Divider, Typography, Button, Stack } from "@mui/material";
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';

import { useEffect, useContext, useState } from "react";

function TeamAnalysisDetailsData({seriesId, gameNumber, team, selectedVisual}) {
    const [side, setSide] = useState("")
    const [value, setValue] = useState([60, 840])
    const [gameEventsAvailable, setGameEventsAvailable] = useState(false)
    const [gameEvents, setGameEvents] = useState([])
    const [gameDuration, setGameDuration] = useState(0)
    const [heatmapsVisible, setHeatmapsVisible] = useState(false)

    let {authTokens} = useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }

    const fetchTeamSide = async () => {
        const data = {
            "seriesId": seriesId,
            "gameNumber": gameNumber,
            "team": team
        }
        
        const result = await fetch(API_URL + `teamAnalysis/getTeamSide/`, {
            method: "PATCH",
            body: JSON.stringify(data),
            headers: header
        })

        result.json().then(data => {
            let newSide = data
            setSide(newSide)
        })
    }

    const fetchGameDuration = async () => {
        const data = {
            "seriesId": seriesId,
            "gameNumber": gameNumber
        }
        const result = await fetch(API_URL + `dataAnalysis/getGameDuration/`, {
            method: "PATCH",
            body: JSON.stringify(data),
            headers: header
        })
        result.json().then(data => {
            let newGameDuration = data
            setGameDuration(newGameDuration)
        })
    }

    const fetchGameEvents = async () => {
        const data = {
            "seriesId": seriesId,
            "gameNumber": gameNumber
        }
        const result = await fetch(API_URL + `dataAnalysis/getGameEvents/`, {
            method: "PATCH",
            body: JSON.stringify(data),
            headers: header
        })
        let newGameEvents = []
        result.json().then(data => {
            data.forEach(element => {
                newGameEvents.push(element)
            })
        })
        setGameEvents(newGameEvents)
        setGameEventsAvailable(true)
    }

    useEffect(() => {
        fetchTeamSide()
        fetchGameDuration()
        fetchGameEvents()
    }, [])

    return (
        <>
            {
                gameEventsAvailable && 
                <>
                    <Stack
                        direction={"row"}
                        spacing={2}
                        alignItems={"center"}
                        justifySelf={"center"}
                        width={"100%"}
                    >
                        <TimeFrameSelecter gameDuration={gameDuration} value={value} setValue={setValue} gameEvents={gameEvents}/>
                        <Button
                            variant="contained"
                            endIcon={<ArrowForwardIosIcon/>}
                            onClick={() => setHeatmapsVisible(true)}
                        >
                            Get Data
                        </Button>
                    </Stack>

                    {
                        heatmapsVisible &&
                        <>
                            {
                                selectedVisual === "Position" && 
                                <>
                                    <Typography variant="h3" component="h3" align="center" sx={{mt: 10, mb:1}}>
                                        Player Position
                                    </Typography>
                                    <Divider
                                        style={{ background: 'white', borderWidth: 1}}
                                        variant="middle"
                                    />
                                    <TeamAnalysisDetailsDataPosition timeFrame={value} seriesId={seriesId} gameNumber={gameNumber} side={side}/>
                                </>
                            }

                            {
                                selectedVisual === "Map Openings" && 
                                <>
                                    <Typography variant="h3" component="h3" align="center" sx={{mt: 10, mb:1}}>
                                        Map Opening
                                    </Typography>
                                    <Divider
                                        style={{ background: 'white', borderWidth: 1}}
                                        variant="middle"
                                    />
                                </>
                            }

                            {
                                selectedVisual === "Reset Position" &&
                                <>
                                    <Typography variant="h3" component="h1" align="center" sx={{mt: 10, mb:1}}>
                                        Reset Position
                                    </Typography>
                                    <Divider
                                        style={{ background: 'white', borderWidth: 1}}
                                        variant="middle"
                                    />
                                    <TeamAnalysisDetailsDataReset timeFrame={value} seriesId={seriesId} gameNumber={gameNumber} side={side}/>
                                </>
                            }

                            {
                                selectedVisual === "Ward Position" && 
                                <>
                                    <Typography variant="h3" component="h1" align="center" sx={{mt: 10, mb:1}}>
                                        Ward Position
                                    </Typography>
                                    <Divider
                                        style={{ background: 'white', borderWidth: 1}}
                                        variant="middle"
                                    />
                                    <TeamAnalysisDetailsDataWard timeFrame={value} seriesId={seriesId} gameNumber={gameNumber} side={side}/>
                                </>
                            }
                            
                            {
                                selectedVisual === "TP Position" && 
                                <>
                                    <Typography variant="h3" component="h1" align="center" sx={{mt: 10, mb:1}}>
                                        TP Position
                                    </Typography>
                                    <Divider
                                        style={{ background: 'white', borderWidth: 1}}
                                        variant="middle"
                                    />
                                    <TeamAnalysisDetailsDataTP timeFrame={value} seriesId={seriesId} gameNumber={gameNumber} side={side}/>
                                </>
                            }
                        </>
                    }
                </>
            }
        </>
    )
}

export default TeamAnalysisDetailsData