import { useState, useEffect, useContext } from "react";

import { API_URL } from "../../constants";
import AuthContext from "../context/AuthContext";
import minimapImage from "../../assets/2dlevelminimap_base_baron1.png";
import ScatterPlot from "../utils/ScatterPlot";

import { Typography } from "@mui/material";

import { Stack } from "react-bootstrap";


function TeamAnalysisDetailsDataTP({timeFrame, seriesId, gameNumber, side}) {
    const [dataTop, setDataTop] = useState([])
    const [dataMid, setDataMid] = useState([])
    const [dataADC, setDataADC] = useState([])
    const [visible, setVisible] = useState(false)

    const bandwidth = 7;  // Adjust this value to change the kernel's spread
    const size = 350

    let {authTokens} = useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }

    const roleList = ["Top", "Mid", "ADC"]

    const fetchPlayerTP = async (position) => {
        const data = {
            "role": position,
            "side": side,
            "seriesId": seriesId,
            "gameNumber": gameNumber,
            "begTime": timeFrame[0],
            "endTime": timeFrame[1]
        }

        const result = await fetch (API_URL + `teamAnalysis/getTPPositions/`, {
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
            if (position === "Top") setDataTop(newDataset)
            if (position === "Mid") setDataMid(newDataset)
            if (position === "ADC") setDataADC(newDataset)
        })
    }

    useEffect(() => {
        roleList.forEach(role => {
            fetchPlayerTP(role)
        })
        setVisible(true)
    }, [])

    return (
        <>
            {
                visible && 
                <div className="wrapper-TeamAnalysisDetailsData">
                   <Stack direction={"columnn"}>
                        <Typography variant="h4" component="h2" align="center" sx={{mb: 1}}>
                            Top
                        </Typography>
                        <ScatterPlot data={dataTop} size={size} backgroundImage={minimapImage} side={side}/>
                    </Stack>
                    <Stack direction={"column"}>
                        <Typography variant="h4" component="h2" align="center" sx={{mb: 1}}>
                            Mid
                        </Typography>
                        <ScatterPlot data={dataMid} size={size} backgroundImage={minimapImage} side={side}/>
                    </Stack>
                    <Stack direction={"column"}>
                        <Typography variant="h4" component="h2" align="center" sx={{mb: 1}}>
                            ADC
                        </Typography>
                        <ScatterPlot data={dataADC} size={size} backgroundImage={minimapImage} side={side}/>
                    </Stack>
                </div>
            }
        </>
    )
}


export default TeamAnalysisDetailsDataTP