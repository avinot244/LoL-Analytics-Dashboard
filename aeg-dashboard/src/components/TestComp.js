import NavBarComp from "./utils/NavbarComp"
import "../styles/TestComp.css"
import Heatmap from "./utils/Heatmap"
import ScatterPlot from "./utils/ScatterPlot"
import minimapImage from "../assets/2dlevelminimap_base_baron1.png"
import AuthContext from "./context/AuthContext"
import TimeFrameSelecter from "./utils/TimeFrameSelecter/TimeFrameSelecter"

import { Typography, Button, Stack } from "@mui/material"
import { useState, useEffect, useContext, useRef } from "react"
import { API_URL, MAP_HEIGHT } from "../constants"


function TestComp() {
    let {authTokens} = useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }

    const size = 350
    // Example data
    const [datasetPosition, setDatasetPosition] = useState([])
    const [datasetReset, setDatasetReset] = useState([])
    const [datasetWardPlaced, setDatasetWardPlaced] = useState([])
    const [value, setValue] = useState([60, 840])
    const [gameEvents, setGameEvents] = useState([])
    const [dataAvailable, setDataAvailable] = useState(false)
    const heatmapRef = useRef(null);

    const handleClearHeatmap = () => {
        if (heatmapRef.current) {
          heatmapRef.current.clearData(); // Call the exposed method
        }
    };

    const fetchPlayerPosition = async () => {
        const data = {
            "role": "Support",
            "side": "Blue",
            "seriesId": 2729017,
            "gameNumber": 1,
            "begTime": value[0],
            "endTime": value[1]
        }

        const result = await fetch(API_URL + `teamAnalysis/getPlayerPosition/`, {
            method: "PATCH",
            body: JSON.stringify(data),
            headers: header
        })

        let newDataset = []
        result.json().then(data => {
            data.forEach(element => {
                newDataset.push({
                    x: Math.ceil(element[0] * size/14750),
                    y: Math.ceil(size - (element[1] * size/14750))
                })
            });
            console.log(newDataset)
            setDatasetPosition(newDataset)
        })
    }

    const fetchResetPositions = async () => {
        const data = {
            "role": "Support",
            "side": "Blue",
            "seriesId": 2729017,
            "gameNumber": 1,
            "begTime": value[0],
            "endTime": value[1]
        }
        const result = await fetch(API_URL + `teamAnalysis/getResetPositions/`, {
            method: "PATCH",
            body: JSON.stringify(data),
            headers: header
        })

        let newDataset = []
        result.json().then(data => {
            data.forEach(element => {
                newDataset.push({
                    x: Math.ceil(element[0] * size/14750),
                    y: Math.ceil(size - (element[1] * size/14750))
                })
            });
            setDatasetReset(newDataset)
        })
    }

    const fetchWardPlaced = async () => {
        const data = {
            "role": "Support",
            "side": "Blue",
            "seriesId": 2729017,
            "gameNumber": 1,
            "begTime": value[0],
            "endTime": value[1],
            "wardType": ["yellowTrinket", "unknown", "control", "sight"]
        }
        const result = await fetch(API_URL + `teamAnalysis/getWardPositions/`, {
            method: "PATCH",
            body: JSON.stringify(data),
            headers: header
        })

        let newDataset = []
        result.json().then(data => {
            data.forEach(element => {
                newDataset.push({
                    x: Math.ceil(element[0] * size/14750),
                    y: Math.ceil(size - (element[1] * size/14750))
                })
            })
            setDatasetWardPlaced(newDataset)
        })
    }

    const fetchGameEvents = async() => {
        const data = {
            "seriesId": 2729017,
            "gameNumber": 1
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
        setDataAvailable(true)
    }

    useEffect(() => {
        fetchGameEvents()
    }, [])
    
    // KDE bandwidth (controls smoothing)
    const bandwidth = 7;  // Adjust this value to change the kernel's spread

    return (
        <div className="wrapper-Test">
            <NavBarComp/>
            <Typography id="title-Test" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold", mb: 10}}>
                Test page
            </Typography>
            {
                dataAvailable &&
                <>
                    <TimeFrameSelecter gameDuration={1626} value={value} setValue={setValue} gameEvents={gameEvents}/>
                    <Button
                        variant="contained"
                        onClick={() => fetchPlayerPosition()}
                    >
                        Get Data Position  
                    </Button>
                    <Button
                        variant="contained"
                        onClick={() => fetchResetPositions()}
                    >
                        Get Data Reset   
                    </Button>
                    <Button
                        variant="contained"
                        onClick={() => fetchWardPlaced()}
                    >
                        Get Data Ward Placed
                    </Button>
                    <Button
                        variant="contained"
                        onClick={() => handleClearHeatmap()}
                    >
                        Clear
                    </Button>

                    <Stack direction={"row"}
                        spacing={2}
                        alignItems={"center"}
                        justifySelf={"center"}
                    >
                        <Heatmap data={datasetPosition} bandwidth={bandwidth} backgroundImage={minimapImage} size={size} ref={heatmapRef} />
                        <ScatterPlot data={datasetReset} backgroundImage={minimapImage} side={"Blue"} size={size} />
                        <ScatterPlot data={datasetWardPlaced} backgroundImage={minimapImage} side={"Blue"} size={size} />
                        <ScatterPlot data={datasetWardPlaced} backgroundImage={minimapImage} side={"Blue"} size={size}/>
                        <ScatterPlot data={datasetWardPlaced} backgroundImage={minimapImage} side={"Blue"} size={size} />
                    </Stack>
                </>
            }
        </div>
    )
}

export default TestComp