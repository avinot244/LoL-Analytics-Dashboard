import NavBarComp from "./utils/NavbarComp"
import "../styles/TestComp.css"
import Heatmap from "./Heatmap"
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
    const [dataset, setDataset] = useState([
    ]);

    // const [dataset, setDataset] = useState([
    // ]);
    
    const data = {
        "playerName": "T1 Oner",
        "seriesId": 2729017,
        "gameNumber": 1,
        "begTime": 60,
        "endTime": 840
    }
    const fetchPlayerPosition = async () => {
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
            setDataset(newDataset)
        })
    }

    
    // KDE bandwidth (controls smoothing)
    const bandwidth = 50;  // Adjust this value to change the kernel's spread

    // Resolution (density resolution, e.g., number of density estimates)
    const resolution = 10;  // Adjust for more/less precision
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
                Get Data    
            </Button>
            <Heatmap data={dataset} bandwidth={bandwidth} resolution={resolution} backgroundImage={minimapImage} />
        </div>
    )
}

export default TestComp