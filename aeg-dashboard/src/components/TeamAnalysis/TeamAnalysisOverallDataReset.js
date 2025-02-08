import { Stack } from "react-bootstrap";

import { useState, useEffect, useContext } from "react";

import { API_URL, roleList, MAP_HEIGHT } from "../../constants";
import AuthContext from "../context/AuthContext";
import ScatterPlot from "../utils/ScatterPlot";
import minimapImage from "../../assets/2dlevelminimap_base_baron1.png";
import "../../styles/TeamAnalysisOverallDataReset.css"

import { Typography } from "@mui/material";

function TeamAnalysisOverallDataReset({timeFrame, team, tournamentList, side}) {
    const [dataTop, setDataTop] = useState(null)
    const [dataJungle, setDataJungle] = useState(null)
    const [dataMid, setDataMid] = useState(null)
    const [dataADC, setDataADC] = useState(null)
    const [dataSupport, setDataSupport] = useState(null)
    const [visible, setVisible] = useState(false)

    const bandwidth = 7;  // Adjust this value to change the kernel's spread
    const size = 350

    let {authTokens} = useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }

    const fetchPlayerReset = async (position) => {
        const data = {
            "role": position,
            "side": side,
            "tournamentList": tournamentList,
            "team": team,
            "begTime": timeFrame[0],
            "endTime": timeFrame[1]
        }

        const result = await fetch(API_URL + "teamAnalysis/getResetPositionsGlobal/", {
            method: "PATCH",
            body: JSON.stringify(data),
            headers: header
        })

        let newDataset = []
        result.json().then(data => {
            data.forEach(element => {
                newDataset.push({
                    x: Math.ceil(element[0] * size/MAP_HEIGHT),
                    y: Math.ceil(size - (element[1] * size/MAP_HEIGHT))
                })
            });
            if (position === "Top") setDataTop(newDataset)
            if (position === "Jungle") setDataJungle(newDataset)
            if (position === "Mid") setDataMid(newDataset)
            if (position === "ADC") setDataADC(newDataset)
            if (position === "Support") setDataSupport(newDataset)
        })
    }

    useEffect(() => {
        roleList.forEach(role => {
            fetchPlayerReset(role)
        })
        setVisible(true)
    }, [])

    return (
        <>
            <div className="wrapper-TeamAnalysisOverallData">
                {
                    dataTop && 
                    <Stack direction={"column"}>
                        <Typography variant="h4" component="h2" align="center" sx={{mb: 1}}>
                            Top
                        </Typography>
                        <ScatterPlot data={dataTop} bandwidth={bandwidth} size={size} side={side} backgroundImage={minimapImage} />
                    </Stack>
                }
                {
                    dataJungle && 
                    <Stack direction={"column"}>
                        <Typography variant="h4" component="h2" align="center" sx={{mb: 1}}>
                            Jungle
                        </Typography>
                        <ScatterPlot data={dataJungle} bandwidth={bandwidth} size={size} side={side} backgroundImage={minimapImage} />
                    </Stack>
                }
                {
                    dataMid && 
                    <Stack direction={"column"}>
                        <Typography variant="h4" component="h2" align="center" sx={{mb: 1}}>
                            Mid
                        </Typography>
                        <ScatterPlot data={dataMid} bandwidth={bandwidth} size={size} side={side} backgroundImage={minimapImage} />
                    </Stack>
                }
                {
                    dataADC && 
                    <Stack direction={"column"}>
                        <Typography variant="h4" component="h2" align="center" sx={{mb: 1}}>
                            ADC
                        </Typography>
                        <ScatterPlot data={dataADC} bandwidth={bandwidth} size={size} side={side} backgroundImage={minimapImage} />
                    </Stack>
                }
                {
                    dataSupport && 
                    <Stack direction={"column"}>
                        <Typography variant="h4" component="h2" align="center" sx={{mb: 1}}>
                            Support
                        </Typography>
                        <ScatterPlot data={dataSupport} bandwidth={bandwidth} size={size} side={side} backgroundImage={minimapImage} />
                    </Stack>
                }
            </div>
        </>
    )

}

export default TeamAnalysisOverallDataReset