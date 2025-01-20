import { API_URL } from "../../constants";
import AuthContext from "../context/AuthContext";
import Heatmap from "../utils/Heatmap";
import ScatterPlot from "../utils/ScatterPlot";
import TimeFrameSelecter from "../utils/TimeFrameSelecter/TimeFrameSelecter";
import { Divider, Typography } from "@mui/material";

import { useEffect, useContext, useState } from "react";

function TeamAnalysisDetailsData({seriesId, gameNumber, team}) {
    // Position Heatmap Top | Position Heatmap Jungle | Position Heatmap Mid | Position Heatmap ADC | Position Heatmap Support
    // Reset Heatmap Top | Reset Heatmap Jungle | Reset Heatmap Mid | Reset Heatmap ADC | Reset Heatmap Support
    // Ward Heatmap Top | Ward Heatmap Jungle | Ward Heatmap Mid | Ward Heatmap ADC | Ward Heatmap Support

    // role : all role will be displayed 
    // side : we do an API request to get the side of the team in the game in the useEffect
    // seriesId : in props
    // gameNumber : in props
    // begTime : selected with the TimeFrameSelecter
    // endTime : selected with the TimeFrameSelected
    // wardTypes : all by default --> add a MultipleSearchComp for it
    const [side, setSide] = useState("")
    const [value, setValue] = useState([60, 840])
    const [gameEventsAvailable, setGameEventsAvailable] = useState(false)
    const [gameEvents, setGameEvents] = useState([])
    const [gameDuration, setGameDuration] = useState(0)

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
        
        const result = await fetch(API_URL + `teamAnalysis/getTeamSide`, {
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
                    <TimeFrameSelecter gameDuration={gameDuration} value={value} setValue={setValue} gameEvents={gameEvents}/>
                    <Typography variant="h3" component="h1" align="center" sx={{mt: 10, mb:1}}>
                        Player Position
                    </Typography>
                    <Divider
                        style={{ background: 'white', borderWidth: 1}}
                        variant="middle"
                    />

                    <Typography variant="h3" component="h1" align="center" sx={{mt: 10, mb:1}}>
                        Reset Position
                    </Typography>
                    <Divider
                        style={{ background: 'white', borderWidth: 1}}
                        variant="middle"
                    />

                    <Typography variant="h3" component="h1" align="center" sx={{mt: 10, mb:1}}>
                        Ward Position
                    </Typography>
                    <Divider
                        style={{ background: 'white', borderWidth: 1}}
                        variant="middle"
                    />
                </>
            }
        </>
    )
}

export default TeamAnalysisDetailsData