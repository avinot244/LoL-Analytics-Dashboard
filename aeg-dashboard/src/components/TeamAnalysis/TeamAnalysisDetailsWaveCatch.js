import { Stack } from "react-bootstrap";

import { useState, useEffect, useContext } from "react";

import { API_URL, roleList } from "../../constants";
import AuthContext from "../context/AuthContext";
import minimapImage from "../../assets/2dlevelminimap_base_baron1.png";
import Heatmap from "../utils/Heatmap";
import "../../styles/TeamAnalysisDetailsDataPosition.css";

import { Typography } from "@mui/material";

function TeamAnalysisDetailWaveCatch({timeFrame, seriesId, gameNumber, side}){
    const [dataTop, setDataTop] = useState([])
    const [dataJungle, setDataJungle] = useState([])
    const [dataMid, setDataMid] = useState([])
    const [dataADC, setDataADC] = useState([])
    const [dataSupport, setDataSupport] = useState([])
    const [visible, setVisible] = useState(false)

    const bandwidth = 2;  // Adjust this value to change the kernel's spread
    const size = 350

    let {authTokens} = useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }

    const fetchPlayerWaveCatch = async (position) => {
        const data = {
            "role": position,
            "side": side,
            "seriesId": seriesId,
            "gameNumber": gameNumber,
            "begTime": timeFrame[0],
            "endTime": timeFrame[1]
        }

        const result = await fetch(API_URL + `teamAnalysis/getSideWaveCatch/`, {
            method: "GET",
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
            if (position === "Jungle") setDataJungle(newDataset)
            if (position === "Mid") setDataMid(newDataset)
            if (position === "ADC") setDataADC(newDataset)
            if (position === "Support") setDataSupport(newDataset)
        })
    }

    useEffect(() => {
        roleList.forEach(role => {
            fetchPlayerWaveCatch(role)
        })
        setVisible(true)
    }, [])

    return (
        <>
            {
                visible &&
                <div className="wrapper-TeamAnalysisDetailsData">
                    <Stack direction={"column"}>
                        <Typography variant="h4" component="h2" align="center" sx={{mb: 1}}>
                            Top
                        </Typography>
                        <Heatmap data={dataTop} bandwidth={bandwidth} size={size} backgroundImage={minimapImage} />
                    </Stack>
                    <Stack direction={"column"}>
                        <Typography variant="h4" component="h2" align="center" sx={{mb: 1}}>
                            Jungle
                        </Typography>
                        <Heatmap data={dataJungle} bandwidth={bandwidth} size={size} backgroundImage={minimapImage} />
                    </Stack>
                    <Stack direction={"column"}>
                        <Typography variant="h4" component="h2" align="center" sx={{mb: 1}}>
                            Mid
                        </Typography>
                        <Heatmap data={dataMid} bandwidth={bandwidth} size={size} backgroundImage={minimapImage} />
                    </Stack>
                    <Stack direction={"column"}>
                        <Typography variant="h4" component="h2" align="center" sx={{mb: 1}}>
                            ADC
                        </Typography>
                        <Heatmap data={dataADC} bandwidth={bandwidth} size={size} backgroundImage={minimapImage} />
                    </Stack>
                    <Stack direction={"column"}>
                        <Typography variant="h4" component="h2" align="center" sx={{mb: 1}}>
                            Support
                        </Typography>
                        <Heatmap data={dataSupport} bandwidth={bandwidth} size={size} backgroundImage={minimapImage} />
                    </Stack>
                </div>
            }
        </>
    )
}

export default TeamAnalysisDetailWaveCatch