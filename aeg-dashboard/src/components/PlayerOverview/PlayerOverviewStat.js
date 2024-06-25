import "../../styles/PlayerOverviewStat.css"
import { API_URL, roleList} from "../../constants";
import { useEffect, useState,useContext } from "react";
import NormalDistribution from "normal-distribution"
import Loading from "../utils/Loading";

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
import { alpha } from '@mui/material/styles';
import { purple } from '@mui/material/colors';
import Divider from "@mui/material/Divider";
import ChampionCard from "./ChampionCard";
import AuthContext from "../context/AuthContext";
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
    const [dataSingleGames, setDataSingleGames] = useState([])

    const [champPoolPickRate, setChampPoolPickRate] = useState([])
    const [champPoolWinRate, setChampPoolWinRate] = useState([])

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
                    setLoading(false)
                    console.log("Finished getting data for tournament patch")

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
                })
            })

            
        }

        const fetchChampionPoolPickRate = async (summonnerName, tournament) => {
            let championPoolPRListTemp = []
            let newChampionPoolPRList = []
            const result = await fetch(API_URL + `draft/playerStat/${summonnerName}/${tournament}/pickRate/`, {
                method: "GET",
                headers:header
            })
            result.json().then(result => {
                for (let i = 0 ; i < result.length ; i++) {
                    let championPoolObject = result[i]
                    let tempDict = {
                        "championName": championPoolObject.championName,
                        "pickRate": (championPoolObject.globalPickRate*100).toFixed(2),
                        "winRate": (championPoolObject.winRate*100).toFixed(2),
                        "nbGames": championPoolObject.nbGames,
                        "kda": championPoolObject.kda.toFixed(2)
                    }
                    championPoolPRListTemp.push(tempDict)
                }
                return championPoolPRListTemp
            }).then(list => {
                newChampionPoolPRList.push(list.slice(0, 6))
                setChampPoolPickRate(newChampionPoolPRList)
            })
        }

        const fetchChampionPoolWinRate = async (summonnerName, tournament) => {
            let championPoolWRListTemp = []
            let newChampionPoolWRList = []
            const result = await fetch(API_URL + `draft/playerStat/${summonnerName}/${tournament}/winRate/`, {
                method: "GET",
                headers:header
            })
            result.json().then(result => {
                for (let i = 0 ; i < result.length ; i++) {
                    let championPoolObject = result[i]
                    let tempDict = {
                        "championName": championPoolObject.championName,
                        "pickRate": (championPoolObject.globalPickRate*100).toFixed(2),
                        "winRate": (championPoolObject.winRate*100).toFixed(2),
                        "nbGames": championPoolObject.nbGames,
                        "kda": championPoolObject.kda.toFixed(2)
                    }
                    championPoolWRListTemp.push(tempDict)
                }
                return championPoolWRListTemp
            }).then(list => {
                newChampionPoolWRList.push(list.slice(0, 6))
                setChampPoolWinRate(newChampionPoolWRList)
            })
        }

        const fetchBehaviorSingleGamesLatest = async (role, summonnerName, limit, wantedTournament) => {
            let uuid = "";
            const modelResult = await fetch(API_URL + `behaviorModels/getModel/${role}/`, {
                method: "GET",
                headers:header
            })
            modelResult.json().then(async model => {
                uuid = model.uuid

                const gamesBehavior = await fetch(API_URL + `behavior/${role}/compute/singleGamesLatest/${summonnerName}/${uuid}/${limit}/${wantedTournament}/${wantedTournament}/`, {
                    method: "GET",
                    headers:header
                })
                gamesBehavior.json().then(result => {
                    const newDataSingleGames = result
                    setDataSingleGames(newDataSingleGames)
                })
            })

            
        }
        
        fetchFactorsPerName()

        fetchBehaviorTournamentPatchPlayer(role, summonnerName, patch, wantedTournament)
        fetchBehaviorTournamentLatestPlayer(role, summonnerName, limit, wantedTournament)
        fetchBehaviorTournamentPlayer(role, summonnerName, wantedTournament)
        fetchBehaviorSingleGamesLatest(role, summonnerName, limit, wantedTournament)

        fetchChampionPoolPickRate(summonnerName, wantedTournament)
        fetchChampionPoolWinRate(summonnerName, wantedTournament)
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

    function getData(behaviorObject, role) {
        if (role === "Top" || role === "Jungle") {
            let result = []
            result.push(behaviorObject.Factor_1[0])
            result.push(behaviorObject.Factor_2[0])
            result.push(behaviorObject.Factor_3[0])
            result.push(behaviorObject.Factor_4[0])
            result.push(behaviorObject.Factor_5[0])
            result.push(behaviorObject.Factor_6[0])
            return result
        }else if (role === "Mid") {
            let result = []
            result.push(behaviorObject.Factor_1[0])
            result.push(behaviorObject.Factor_2[0])
            result.push(behaviorObject.Factor_3[0])
            result.push(behaviorObject.Factor_4[0])
            result.push(behaviorObject.Factor_5[0])
            result.push(behaviorObject.Factor_6[0])
            result.push(behaviorObject.Factor_7[0])
            result.push(behaviorObject.Factor_8[0])
            return result
        }else if (role === "ADC") {
            let result = []
            result.push(behaviorObject.Factor_1[0])
            result.push(behaviorObject.Factor_2[0])
            result.push(behaviorObject.Factor_3[0])
            result.push(behaviorObject.Factor_4[0])
            return result
        }else if (role === "Support") {
            let result = []
            result.push(behaviorObject.Factor_1[0])
            result.push(behaviorObject.Factor_2[0])
            result.push(behaviorObject.Factor_3[0])
            result.push(behaviorObject.Factor_4[0])
            result.push(behaviorObject.Factor_5[0])
            result.push(behaviorObject.Factor_6[0])
            result.push(behaviorObject.Factor_7[0])
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
                        
        },
        {
            label: `Behavior ${summonnerName} latest ${limit} games at ${wantedTournament}`,
            data: dataBehaviorLatest,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgb(54, 162, 235)',
            borderWidth: 1,
        },
        {
            label: `Behavior ${summonnerName} at ${wantedTournament}`,
            data: dataBehaviorTournament,
            backgroundColor: 'rgba(74, 191, 192, 0.2)',
            borderColor: 'rgb(74, 191, 192)',
            borderWidth: 1,
        }
    ]

    for (let i = 0 ; i < dataSingleGames.length ; i++) {
        let temp = {
            label: `Behavior ${summonnerName} game ${dataSingleGames.length - i}`,
            data: getData(dataSingleGames[i], role),
            backgroundColor: alpha(purple[100*(2*i+1)], 0.2),
            borderColor: purple[100*(2*i+1)],
            borderWidth: 1,
        }
        behaviorDatasets.push(temp)
    }

    const data = {
        labels: factorsNamePerRole[role],
        datasets: behaviorDatasets,
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
                    color: (context) => {
                        if (context.tick.value === 0) {
                            return "#d32f2f"
                        } else {
                            return "#fff"
                        }
                    },
                    lineWidth: (context) => {
                        console.log(context)
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
                    {
                        loading ? (
                            <Loading />
                        ) : (
                            <div className="playerOverview-graph">
                                <Radar
                                    data={data}
                                    options={options}
                                />
                            </div>

                        )
                    }
                    
            </div>

            <br />

            <Divider
                style={{ background: 'white', borderWidth: 1}}
                variant="middle"
            />

            <div className="playerOverview-other-content">
                <br/>
                <div className="playerOverview-champs">
                    <h2>Best champions by pick rate</h2>
                    {
                        champPoolPickRate.length > 0 && 
                        <ul className="playerOverview-champion-list">
                            {champPoolPickRate[0].map((object) => 
                                <ChampionCard
                                    championName={object.championName}
                                    pickRate={object.pickRate}
                                    winRate={object.winRate}
                                    nbGames={object.nbGames}
                                    kda={object.kda}
                                />
                            )}
                        </ul>
                    }
                    

                    <h2>Best champions by win rate</h2>
                    {
                        champPoolWinRate.length > 0 && 
                        <ul className="playerOverview-champion-list">
                            {champPoolWinRate[0].map((object) => 
                                <ChampionCard
                                    championName={object.championName}
                                    pickRate={object.pickRate}
                                    winRate={object.winRate}
                                    nbGames={object.nbGames}
                                    kda={object.kda}
                                />
                            )}
                        </ul>
                    }
                </div>
            </div>
        </div>
    )
}