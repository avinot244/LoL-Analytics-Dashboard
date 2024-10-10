import "../../styles/PlayerOverviewStat.css"
import { API_URL, roleList} from "../../constants";
import Loading from "../utils/Loading";
import RedSwitch from "../utils/switches/RedSwitch.js"
import BlueSwitch from "../utils/switches/BlueSwitch.js"
import TealSwith from "../utils/switches/TealSwitch.js"

import { useEffect, useState,useContext } from "react";
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
import AuthContext from "../context/AuthContext";
import { FormControlLabel, FormGroup } from "@mui/material";
ChartJS.register(
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend,
);


export default function PlayerOverviewStat(props) {
    const {role, summonnerName, patch, wantedTournament, limit} = props

    const [dataBehaviorPatch, setDataBehaviorPatch] = useState([])
    const [dataBehaviorLatest, setDataBehaviorLatest] = useState([])
    const [dataBehaviorTournament, setDataBehaviorTournament] = useState([])

    const [displayDataTournament, setDisplayDataTournament] = useState(true)
    const [displayDataPatch, setDisplayDataPatch] = useState(false)
    const [displayDataLatest, setDisplayDataLatest] = useState(false)

    const [factorsNamePerRole, setFactorsNamePerRole] = useState({
        "Top": [],
        "Jungle": [],
        "Mid": [],
        "ADC": [],
        "Support": []
    })

    const [loading, setLoading] = useState(true)

    let {authTokens} = useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }

    useEffect(() => {
        const fetchFactorsPerName = async () => {
            let newFactorsNamePerRole = factorsNamePerRole
            roleList.map(async (role) => {
                const model = await fetch(API_URL + `behaviorModels/getModel/${role}/`, {
                    method: "GET",
                    headers:header
                })
                model.json().then(model => {
                    newFactorsNamePerRole[role] = JSON.parse(model.factorsName.replace(/'/g, '"'))
                })
            })
            setFactorsNamePerRole(newFactorsNamePerRole)
        }    
    
        const fetchBehaviorTournamentPatchPlayer = async (role, summonnerName, patch, wantedTournament) => {
            setLoading(true)
            let uuid = "";
            const modelResult = await fetch(API_URL + `behaviorModels/getModel/${role}/`, {
                method: "GET",
                headers:header
            })
            modelResult.json().then(async model => {
                uuid = model.uuid

                const result = await fetch(API_URL + `behavior/${role}/compute/${summonnerName}/${patch}/${uuid}/${wantedTournament}/${wantedTournament}/`, {
                method: "GET",
                headers:header
                })
                result.json().then(result => {
                    const newBehaviorPatch = result
                    setDataBehaviorPatch(getAvgData(newBehaviorPatch, role))
                    

                })
            })            
        }

        const fetchBehaviorTournamentLatestPlayer = async (role, summonnerName, limit, wantedTournament) => {
            let uuid = "";
            const modelResult = await fetch(API_URL + `behaviorModels/getModel/${role}/`, {
                method: "GET",
                headers:header
            })
            modelResult.json().then(async model => {
                uuid = model.uuid

                const result = await fetch(API_URL + `behavior/${role}/compute/${summonnerName}/${limit}/${uuid}/${wantedTournament}/${wantedTournament}/`, {
                    method: "GET",
                    headers:header
                })
                result.json().then(result => {
                    const newBehaviorLatest = result
                    setDataBehaviorLatest(getAvgData(newBehaviorLatest, role))
                })
            })

            
        }

        const fetchBehaviorTournamentPlayer = async (role, summonnerName, wantedTournament) => {
            let uuid = "";
            const modelResult = await fetch(API_URL + `behaviorModels/getModel/${role}/`, {
                method: "GET",
                headers:header
            })
            modelResult.json().then(async model => {
                uuid = model.uuid
                const result = await fetch(API_URL + `behavior/${role}/compute/${summonnerName}/${uuid}/${wantedTournament}/${wantedTournament}/`, {
                    method: "GET",
                    headers:header
                })
                result.json().then(result => {
                    const newBehaviorTournament = result
                    setDataBehaviorTournament(getAvgData(newBehaviorTournament, role))
                    setLoading(false)
                })
            })

            
        }
        
        fetchFactorsPerName()
        fetchBehaviorTournamentPatchPlayer(role, summonnerName, patch, wantedTournament)
        fetchBehaviorTournamentLatestPlayer(role, summonnerName, limit, wantedTournament)
        fetchBehaviorTournamentPlayer(role, summonnerName, wantedTournament)

        
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


    let behaviorDatasets = [
        {
            label: `Behavior ${summonnerName} during patch ${patch} at ${wantedTournament}`,
            data: dataBehaviorPatch,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgb(255, 99, 132)',
            borderWidth: 1,
            hidden: !(displayDataPatch)
                        
        },
        {
            label: `Behavior ${summonnerName} latest ${limit} games at ${wantedTournament}`,
            data: dataBehaviorLatest,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgb(54, 162, 235)',
            borderWidth: 1,
            hidden: !(displayDataLatest)
        },
        {
            label: `Behavior ${summonnerName} at ${wantedTournament}`,
            data: dataBehaviorTournament,
            backgroundColor: 'rgba(74, 191, 192, 0.2)',
            borderColor: 'rgb(74, 191, 192)',
            borderWidth: 1,
            hidden: !(displayDataTournament)
        }
    ]

    const data = {
        labels: factorsNamePerRole[role],
        datasets: behaviorDatasets,
    }

    const computeMax = () => {
        const maxPatch = Math.max(...dataBehaviorPatch)
        const maxLatest = Math.max(...dataBehaviorLatest)
        const maxTournament = Math.max(...dataBehaviorTournament)

        const max = Math.max(maxPatch, maxLatest, maxTournament)
        if (max > 2.33) {
            return 2.33
        }
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
                    color: (context) => {
                        if (context.tick.value === 0) {
                            return "#d32f2f"
                        } else {
                            return "#fff"
                        }
                    },
                    lineWidth: (context) => {
                        if (context.tick.value === 0) {
                            return 4
                        } else {
                            return 1
                        }
                    }
                },
                pointLabels: {
                    color: "#FFF"
                }
            },
        },
        plugins: {
            legend: {
                display: false,
                // labels: {
                //     color: '#FFF'
                // }
            },
            customCanvasBackgroundColor: {
                color: 'black'
            }
        }
    }



    return (
        <div className="playerOverview-content-wrapper">
            <div className="playerOverviewGraph">
                {
                    loading ? (
                        <Loading />
                    ) : (
                        <div className="playerOverview-graph">
                            <h1>{summonnerName}</h1>
                            <FormGroup row>
                                <FormControlLabel control={<RedSwitch onChange={(event => {setDisplayDataPatch(event.target.checked)})}/>} label={`Patch ${patch}`}/>
                                <FormControlLabel control={<BlueSwitch onChange={(event => {setDisplayDataLatest(event.target.checked)})}/>} label={`Latest ${limit} Games`}/>
                                <FormControlLabel control={<TealSwith defaultChecked onChange={(event => {setDisplayDataTournament(event.target.checked)})}/>} label={`${wantedTournament}`}/>
                            </FormGroup>
                            <Radar
                                data={data}
                                options={options}
                            />
                        </div>
                    )
                } 
            </div>        
        </div>
    )
}