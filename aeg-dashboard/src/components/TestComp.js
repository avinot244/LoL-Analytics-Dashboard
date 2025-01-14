import NavBarComp from "./utils/NavbarComp"
import "../styles/TestComp.css"
import Heatmap from "./utils/Heatmap"
import ScatterPlot from "./utils/ScatterPlot"
import minimapImage from "../assets/2dlevelminimap_base_baron1.png"
import AuthContext from "./context/AuthContext"
import TimeFrameSelecter from "./utils/TimeFrameSelecter/TimeFrameSelecter"

import { Typography, Button, Stack } from "@mui/material"
import { useState, useEffect, useContext } from "react"
import { API_URL, MAP_HEIGHT } from "../constants"


function TestComp() {
    let {authTokens} = useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }
    // Example data
    const [datasetPosition, setDatasetPosition] = useState([])
    const [datasetReset, setDatasetReset] = useState([])
    const [datasetWardPlaced, setDatasetWardPlaced] = useState([])
    const [value, setValue] = useState([60, 840])
    const [flagDisplayHeatmaps, setFlagDisplayHeatmaps] = useState(true)
    
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
                    x: Math.ceil(element[0] * 10/295),
                    y: Math.ceil(500 - (element[1] * 10/295))
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
                    x: Math.ceil(element[0] * 10/295),
                    y: Math.ceil(500 - (element[1] * 10/295))
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
                    x: Math.ceil(element[0] * 10/295),
                    y: Math.ceil(500 - (element[1] * 10/295))
                })
            })
            setDatasetWardPlaced(newDataset)
        })
    }

    const handleReset = () => {
        setFlagDisplayHeatmaps(false)
        setDatasetPosition([])
        setDatasetReset([])
        setDatasetWardPlaced([])
        setFlagDisplayHeatmaps(true)
    }

    
    // KDE bandwidth (controls smoothing)
    const bandwidth = 7;  // Adjust this value to change the kernel's spread

    return (
        <div className="wrapper-Test">
            <NavBarComp/>
            <Typography id="title-Test" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold", mb: 10}}>
                Test page
            </Typography>
            <TimeFrameSelecter gameDuration={1626} value={value} setValue={setValue}/>


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
                onClick={() => handleReset()}
            >
                Reset
            </Button>

            <Stack spacing={2} direction="row" justifyContent="space-between" alignItems="center" sx={{mr: 10, ml: 10}}>
                <Heatmap data={datasetPosition} bandwidth={bandwidth} backgroundImage={minimapImage} />
                <ScatterPlot data={datasetReset} backgroundImage={minimapImage} side={"Blue"}/>
                <ScatterPlot data={datasetWardPlaced} backgroundImage={minimapImage} side={"Blue"}/>
            </Stack>
            
        </div>
    )
}

export default TestComp