import ChampionCard from "./ChampionCard"
import { useEffect, useState, useContext } from "react"

import { API_URL } from "../../constants"
import AuthContext from "../context/AuthContext";

function PlayerOverviewChampPool({summonnerName, tournament}) {

    const [champPoolPickRate, setChampPoolPickRate] = useState([])
    const [champPoolWinRate, setChampPoolWinRate] = useState([])

    let {authTokens} = useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
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
            newChampionPoolPRList.push(list.slice(0, 5))
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
            newChampionPoolWRList.push(list.slice(0, 5))
            setChampPoolWinRate(newChampionPoolWRList)
        })
    }


    useEffect(() => {
        fetchChampionPoolPickRate(summonnerName, tournament)
        fetchChampionPoolWinRate(summonnerName, tournament)
    }, [])

    return (
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
    )
}

export default PlayerOverviewChampPool