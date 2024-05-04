import "../../styles/PlayerOverviewStat.css"
import { API_URL, behaviorModelUUID, factorNamePerRole} from "../../constants";
import { useEffect, useState } from "react";
import NormalDistribution from "normal-distribution"

import {
    Chart as ChartJS,
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend,
} from 'chart.js';
import { Radar } from 'react-chartjs-2';
import { FormControlLabel, FormGroup, Switch } from "@mui/material";
import { alpha, styled } from '@mui/material/styles';
import { blue, teal, red, yellow, purple } from '@mui/material/colors';
import Divider from "@mui/material/Divider";
import ChampionCard from "./ChampionCard";
ChartJS.register(
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend,
);

const BlueSwitch = styled(Switch)(({ theme }) => ({
    '& .MuiSwitch-switchBase.Mui-checked': {
        color: blue[600],
        '&:hover': {
            backgroundColor: alpha(blue[600], theme.palette.action.hoverOpacity),
        },
    },
    '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
        backgroundColor: blue[600],
    },
}));

const TealSwitch = styled(Switch)(({ theme }) => ({
    '& .MuiSwitch-switchBase.Mui-checked': {
        color: teal[600],
        '&:hover': {
            backgroundColor: alpha(teal[600], theme.palette.action.hoverOpacity),
        },
    },
    '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
        backgroundColor: teal[600],
    },
}));

const RedSwitch = styled(Switch)(({ theme }) => ({
    '& .MuiSwitch-switchBase.Mui-checked': {
        color: red[600],
        '&:hover': {
            backgroundColor: alpha(red[600], theme.palette.action.hoverOpacity),
        },
    },
    '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
        backgroundColor: red[600],
    },
}));

export default function PlayerOverviewStat(props) {
    const {role, summonnerName, patch, wantedTournament, limit} = props

    const [dataBehaviorPatch, setDataBehaviorPatch] = useState([])
    const [dataBehaviorLatest, setDataBehaviorLatest] = useState([])
    const [dataBehaviorTournament, setDataBehaviorTournament] = useState([])

    const [displayPatch, setDisplayPatch] = useState(true)
    const [displayLatest, setDisplayLatest] = useState(true)
    const [displayTournament, setDisplayTournament] = useState(true)

    const gd15 = 450
    const k15 = 4
    const d15 = 1
    const a15 = 5

    const championList = ["Hwei", "Thresh", "Leona", "Maokai", "Senna", "Nautilus"]

    useEffect(() => {
        const fetchBehaviorTournamentPatchPlayer = async (role, summonnerName, patch, wantedTournament) => {
            const result = await fetch(API_URL + `behavior/${role}/compute/${summonnerName}/${patch}/${behaviorModelUUID}/${wantedTournament}/${wantedTournament}/`, {
                method: "GET"
            })
            result.json().then(result => {
                const newBehaviorPatch = result
                console.log(newBehaviorPatch)
                setDataBehaviorPatch(getAvgData(newBehaviorPatch, role))
            })
        }

        const fetchBehaviorTournamentLatestPlayer = async (role, summonnerName, limit, wantedTournament) => {
            const result = await fetch(API_URL + `behavior/${role}/compute/${summonnerName}/${limit}/${behaviorModelUUID}/${wantedTournament}/${wantedTournament}/`, {
                method: "GET"
            })
            result.json().then(result => {
                const newBehaviorLatest = result
                console.log(newBehaviorLatest)
                setDataBehaviorLatest(getAvgData(newBehaviorLatest, role))
            })
        }

        const fetchBehaviorTournamentPlayer = async (role, summonnerName, wantedTournament) => {
            const result = await fetch(API_URL + `behavior/${role}/compute/${summonnerName}/${behaviorModelUUID}/${wantedTournament}/${wantedTournament}/`, {
                method: "GET"
            })
            result.json().then(result => {
                const newBehaviorTournament = result
                console.log(newBehaviorTournament)
                setDataBehaviorTournament(getAvgData(newBehaviorTournament, role))
            })
        }


        fetchBehaviorTournamentPatchPlayer(role, summonnerName, patch, wantedTournament)
        fetchBehaviorTournamentLatestPlayer(role, summonnerName, limit, wantedTournament)
        fetchBehaviorTournamentPlayer(role, summonnerName, wantedTournament)
        console.log(dataBehaviorLatest)
        console.log(dataBehaviorPatch)
        console.log(dataBehaviorTournament)

    }, [])

    function getAvgData(behaviorObject, role) {
        if (role === "Top") {
            let result = []
            let sum = behaviorObject.Factor_1.reduce((a, b) => a + b, 0)
            let temp = result.push(sum / behaviorObject.Factor_1.length)

            sum = behaviorObject.Factor_2.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_2.length)

            sum = behaviorObject.Factor_3.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_3.length)

            sum = behaviorObject.Factor_4.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_4.length)

            sum = behaviorObject.Factor_5.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_5.length)

            sum = behaviorObject.Factor_6.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_6.length)
            return result
        }else if (role === "Jungle") {
            let result = []
            let sum = behaviorObject.Factor_1.reduce((a, b) => a + b, 0)
            let temp = result.push(sum / behaviorObject.Factor_1.length) || 0

            sum = behaviorObject.Factor_2.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_2.length) || 0

            sum = behaviorObject.Factor_3.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_3.length) || 0

            sum = behaviorObject.Factor_4.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_4.length) || 0

            sum = behaviorObject.Factor_5.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_5.length) || 0

            sum = behaviorObject.Factor_6.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_6.length) || 0
            return result
        }else if (role === "Mid") {
            let result = []
            let sum = behaviorObject.Factor_1.reduce((a, b) => a + b, 0)
            let temp = result.push(sum / behaviorObject.Factor_1.length) || 0

            sum = behaviorObject.Factor_2.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_2.length) || 0

            sum = behaviorObject.Factor_3.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_3.length) || 0

            sum = behaviorObject.Factor_4.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_4.length) || 0

            sum = behaviorObject.Factor_5.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_5.length) || 0

            sum = behaviorObject.Factor_6.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_6.length) || 0

            sum = behaviorObject.Factor_7.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_7.length) || 0

            sum = behaviorObject.Factor_8.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_8.length) || 0
            return result
        }else if (role === "ADC") {
            let result = []
            let sum = behaviorObject.Factor_1.reduce((a, b) => a + b, 0)
            let temp = result.push(sum / behaviorObject.Factor_1.length) || 0

            sum = behaviorObject.Factor_2.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_2.length) || 0

            sum = behaviorObject.Factor_3.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_3.length) || 0

            sum = behaviorObject.Factor_4.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_4.length) || 0
            return result
        }else if (role === "Support") {
            let result = []
            let sum = behaviorObject.Factor_1.reduce((a, b) => a + b, 0)
            let temp = result.push(sum / behaviorObject.Factor_1.length) || 0

            sum = behaviorObject.Factor_2.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_2.length) || 0

            sum = behaviorObject.Factor_3.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_3.length) || 0

            sum = behaviorObject.Factor_4.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_4.length) || 0

            sum = behaviorObject.Factor_5.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_5.length) || 0

            sum = behaviorObject.Factor_6.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_6.length) || 0

            sum = behaviorObject.Factor_7.reduce((a, b) => a + b, 0)
            temp = result.push(sum / behaviorObject.Factor_7.length) || 0
            return result
        }
    }
    
    const data = {
        labels: factorNamePerRole[role],
        datasets: [
            {
                label: `Behavior ${summonnerName} during patch ${patch} at ${wantedTournament}`,
                data: dataBehaviorPatch,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgb(255, 99, 132)',
                borderWidth: 1,
                hidden: !displayPatch
                            
            },
            {
                label: `Behavior ${summonnerName} latest ${limit} games at ${wantedTournament}`,
                data: dataBehaviorLatest,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgb(54, 162, 235)',
                borderWidth: 1,
                hidden: !displayLatest
            },
            {
                label: `Behavior ${summonnerName} at ${wantedTournament}`,
                data: dataBehaviorTournament,
                backgroundColor: 'rgba(74, 191, 192, 0.2)',
                borderColor: 'rgb(74, 191, 192)',
                borderWidth: 1,
                hidden: !displayTournament
            }
        ]
    }

    const computeMax = () => {
        const maxPatch = Math.max(...dataBehaviorPatch)
        const maxLatest = Math.max(...dataBehaviorLatest)
        const maxTournament = Math.max(...dataBehaviorTournament)

        const max = Math.max(maxPatch, maxLatest, maxTournament)
        if (max > 1.5) {
            return Math.ceil(max)
        }else{
            return 1.5
        }

    }

    const computeMin = () => {
        const minPatch = Math.min(...dataBehaviorPatch)
        const minLatest = Math.min(...dataBehaviorLatest)
        const minTournament = Math.min(...dataBehaviorTournament)

        const min = Math.min(minPatch, minLatest, minTournament)
        if (min < -1.5) {
            return Math.floor(min)
        }else{
            return -1.5
        }
    }

    const options = {
        scales: {
            r: {
                max: computeMax(),
                min: computeMin(),
                ticks: {
                    stepSize: 0.5,
                    color: '#FFF',
                    backdropColor: 'rgba(0, 0, 0, 0)',
                    callback: (value, tick, values) => {
                        const normDist = new NormalDistribution(0, 1)

                        return `${((1-normDist.cdf(value))*100).toFixed(2)}%`
                    }
                },
                angleLines: {
                    display: true,
                    color: "#FFF"
                },
                grid: {
                    display: true,
                    color: "#FFF"
                },
                pointLabels: {
                    color: "#FFF"
                }
            },
        },
        plugins: {
            legend: {
                display: true,
                labels: {
                    color: '#FFF'
                }
            },
            customCanvasBackgroundColor: {
                color: 'black'
            }
        }
    }



    return (
        <div className="playerOverview-content-wrapper">
            <div className="playerOverviewGraph">
                <div className="graph-ControlPanel">
                    <FormGroup row>
                        <FormControlLabel control={<RedSwitch defaultChecked onChange={(event) => {setDisplayPatch(event.target.checked)}}/>} label={`Patch ${patch}`}/>
                        <FormControlLabel control={<BlueSwitch defaultChecked onChange={(event) => {setDisplayLatest(event.target.checked)}}/>} label={`Latest ${limit} games`}/>
                        <FormControlLabel control={<TealSwitch defaultChecked onChange={(event) => {setDisplayTournament(event.target.checked)}}/>} label={`Tournament`}/>
                    </FormGroup>
                </div>

                <div className="playerOverview-graph">
                    <Radar
                        data={data}
                        options={options}
                    />
                </div>
            </div>

            <br />

            <Divider
                style={{ background: 'white', borderWidth: 1}}
                variant="middle"
            />

            <div className="playerOverview-other-content">
                <div className="playerOverview-stats">
                    <h2>Overall stats</h2>
                    <div className="playerOverview-stats-GD">
                        <p>
                            AVG GD@15 : {gd15 > 0 ? `+${gd15} golds` : `-${gd15} golds`}
                        </p>
                    </div>
                    <div className="playerOverview-stats-kda">
                        <p>
                            AVG K/D/A@15 : {`${k15}/${d15}/${a15}`}
                        </p>
                    </div>  
                </div>
                <br/>
                <div className="playerOverview-champs">
                    <h2>Best champs by pick rate</h2>
                    <ul className="playerOverview-champion-list">
                        {championList.map((championName) => 
                            <ChampionCard
                                championName={championName}
                                pickRate={50}
                                winRate={50}
                                nbGames={10}
                                kda={2.5}
                            />
                        )}
                    </ul>

                    <h2>Best champs by win rate</h2>
                    <ul className="playerOverview-champion-list">
                        {championList.map((championName) => 
                            <ChampionCard
                                championName={championName}
                                pickRate={50}
                                winRate={50}
                                nbGames={10}
                                kda={2.5}
                            />
                        )}
                    </ul>
                </div>
            </div>
        </div>
    )
}