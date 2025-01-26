import ObjectiveCard from "./ObjectiveCard"
import TimeFrameSelecterNoEvent from "../utils/TimeFrameSelecter/TimeFrameSelecterNoEvents";
import TeamAnalysisOverallDataReset from "./TeamAnalysisOverallDataReset";
import SelectComp from "../utils/SelectComp";
import { API_URL } from "../../constants";

import { Button, Stack } from "@mui/material"
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import RestartAltIcon from '@mui/icons-material/RestartAlt';

import { useState } from "react";

import HeatMap from "react-heatmap-grid";

import "../../styles/TeamAnalysisOverall.css"



function TeamAnalysisOverallData ({dataGrubsDrakes, dataFirstTowerHerald, dataHerald, dataFirstTower, gameDurationOverall, team, tournamentList}) {
    const [value, setValue] = useState([90, 840])
    const [visible, setVisible] = useState(false)
    const [activeSide, setActiveSide] = useState("Blue")
    const side = ["Blue", "Red", "Both"];
    let yLabels = []
    for (let i = 0 ; i < 5 ; i++) {
        yLabels.push(`${i} drakes`)
    }

    let xLabels = []
    for (let i = 0 ; i < 7 ; i++) {
        xLabels.push(`${i} grubs`)
    }
    
    let data = []

    for (let i = 0 ; i < dataGrubsDrakes.length ; i++) {
        let tempData = []
        for (let j = 0 ; j < dataGrubsDrakes[i].length ; j ++) {
            tempData.push(dataGrubsDrakes[i][j].winRate)
        }
        data.push(tempData)
    }

    return (
        <div className="teamAnalysisOverallData">
            <Stack direction={"row"} spacing={5} justifyContent="center" alignItems="center" sx={{mt: 5}}>
                <ObjectiveCard 
                    objectiveName={"First Tower Winrate"}
                    nbGames={dataFirstTower.totalGames}
                    winRate={(dataFirstTower.winRate*100).toFixed(2)}
                    nbWin={dataFirstTower.totalWins}
                    media={false}
                />

                <ObjectiveCard 
                    objectiveName={"Herald Winrate"}
                    nbGames={dataHerald.totalGames}
                    winRate={(dataHerald.winRate*100).toFixed(2)}
                    nbWin={dataHerald.totalWins}
                    media={false}
                />

                <ObjectiveCard
                    objectiveName={"Herald over First Tower Winrate"}
                    nbGames={dataFirstTowerHerald.totalGames}
                    winRate={(dataFirstTowerHerald.winRate*100).toFixed(2)}
                    nbWin={dataFirstTowerHerald.totalWins}
                    media={false}
                />
            </Stack>
            <div className="wrapper-heatmap-teamAnalysisOverall">
                {
                    data.length === 5 &&
                    <HeatMap
                        xLabels={xLabels}
                        yLabels={yLabels}
                        xLabelWidth={100}
                        yLabelWidth={100}
                        data={data}
                        height={50}
                        onClick={(x, y) => alert(`Nb Games : ${dataGrubsDrakes[y][x].totalGames}\nNb Wins : ${dataGrubsDrakes[y][x].totalWins}`)}
                        cellStyle={(background, value, min, max, data, x, y) => ({
                            background: `rgb(0, 151, 230, ${1 - (max - value) / (max - min)})`,
                            fontSize: "11.5px",
                            color: "white"
                        })}
                        cellRender={value => value && <div>{(value*100).toFixed(2)}%</div>}
                    />
                }
            </div>
            <Stack direction={"row"} spacing={5} justifyContent="center" alignItems="center" sx={{mt: 5}}>
                <TimeFrameSelecterNoEvent
                    value={value}
                    setValue={setValue}
                    gameDuration={gameDurationOverall}
                />
                <Button
                    variant="contained"
                    endIcon={<ArrowForwardIosIcon/>}
                    onClick={() => {
                        setVisible(true)
                    }}
                >
                    Analyze
                </Button>
                <Button
                    variant="contained"
                    endIcon={<RestartAltIcon/>}
                    onClick={() => {
                        setVisible(false)
                    }}
                >
                    Reset
                </Button>
            </Stack>
            
            {
                visible && 
                <>
                    <TeamAnalysisOverallDataReset
                        team={team}
                        tournamentList={tournamentList}
                        side={"Blue"}
                        timeFrame={value}
                        
                    />
                    {/* <TeamAnalysisOverallDataReset
                        team={team}
                        tournamentList={tournamentList}
                        side={"Red"}
                        begTime={value[0]}
                        endTime={value[1]}
                    /> */}
                </>
                
            }
            
        </div>
    )
}

export default TeamAnalysisOverallData