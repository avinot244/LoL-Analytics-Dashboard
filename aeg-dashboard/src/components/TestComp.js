import NavBarComp from "./utils/NavbarComp"
import "../styles/TestComp.css"
import Heatmap from "./utils/Heatmap"
import ScatterPlot from "./utils/ScatterPlot"
import minimapImage from "../assets/2dlevelminimap_base_baron1.png"
import AuthContext from "./context/AuthContext"

import { Typography, Button } from "@mui/material"
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

    // const [dataset, setDataset] = useState([
    // ]);
    
    
    const fetchPlayerPosition = async () => {
        const data = {
            "role": "Jungle",
            "side": "Blue",
            "seriesId": 2729017,
            "gameNumber": 1,
            "begTime": 60,
            "endTime": 840
        }

        const result = await fetch(API_URL + `dataAnalysis/getPlayerPosition/`, {
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
            "role": "Jungle",
            "side": "Blue",
            "seriesId": 2729017,
            "gameNumber": 1,
            "begTime": 60,
            "endTime": 840
        }
        const result = await fetch(API_URL + `dataAnalysis/getResetPositions/`, {
            method: "PATCH",
            body: JSON.stringify(data),
            headers: header
        })

        let newDataset = []
        console.log(result)
        result.json().then(data => {
            data.forEach(element => {
                newDataset.push({
                    x: Math.ceil(element[0] * 10/295),
                    y: Math.ceil(500 - (element[1] * 10/295))
                })
            });
            console.log(newDataset)
            setDatasetReset(newDataset)
        })
    }

    
    // KDE bandwidth (controls smoothing)
    const bandwidth = 7;  // Adjust this value to change the kernel's spread

    // Resolution (density resolution, e.g., number of density estimates)
    return (
        <div className="wrapper-Test">
            <NavBarComp/>
            <Typography id="title-Test" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold", mb: 10}}>
                Test page
            </Typography>
            <Button
                variant="contained"
                onClick={() => fetchPlayerPosition()}
            >
                Get Data Position  
            </Button>
            <Button
                variant="contained"
                onClick={() => fetchResetPositions([])}
            >
                Get Data Reset   
            </Button>
            <Heatmap data={datasetPosition} bandwidth={bandwidth} backgroundImage={minimapImage} />
            <ScatterPlot data={datasetReset} backgroundImage={minimapImage} side={"Blue"}/>
        </div>
    )
}

export default TestComp