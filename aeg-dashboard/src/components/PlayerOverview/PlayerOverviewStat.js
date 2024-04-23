import "../../styles/PlayerOverviewStat.css"
import ChampionIcon from "../ChampionIcon";
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
        fetchBehaviorTournamentPatchPlayer(role, summonnerName, patch, wantedTournament)
        fetchBehaviorTournamentLatestPlayer(role, summonnerName, limit, wantedTournament)

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
                            
            },
            {
                label: `Behavior ${summonnerName} latest ${limit} games at ${wantedTournament}`,
                data: dataBehaviorLatest,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgb(54, 162, 235)',
                borderWidth: 1,
            }
        ]
    }

    const options = {
        scales: {
            r: {
                max: 1.5,
                min: -1.5,
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
            <div className="playerOverview-graph">
                <Radar
                    data={data}
                    options={options}
                />
            </div>
            
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
                    <h2>Best champs</h2>
                    <ul className="playerOverview-champion-list">
                        {championList.map((championName) => 
                            <ChampionIcon
                                championName={championName}
                                winRate={50}
                                pickRate={60}
                                banRate={30}
                                pickOrder={1}
                            />
                        )}
                    </ul>
                </div>
            </div>
        </div>
    )
}