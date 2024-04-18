import { API_URL, roleList } from "../constants";
import ChampionIcon from "./ChampionIcon";
import { useState, useEffect } from "react";

export default function ChampionOverviewListPanel(props) {
    const {filter, side, patch, tournament} = props

    const [championList, setChampionList] = useState([])
    const [flagDisplay, setFlagDisplay] = useState(false)
    const fetchTopMetaPicks = async () => {
        let newChampionList = []
        
        for (let i = 0 ; i < roleList.length ; i++) {
            let championListTemp = []
            const result = await fetch(API_URL + `draft/championStats/getTopChampions/${roleList[i]}/${filter}/${side}/${patch}/${tournament}/`, {
                method: "GET"
            })
            result.json().then(result => {
                for (let i = 0 ; i < result.length ; i++) {
                    let championStatsObject = result[i]
                    let tempDict = {
                        "championName": championStatsObject.championName,
                        "winRate": (championStatsObject.winRate*100).toFixed(2),
                        "pickRate": (championStatsObject.globalPickRate*100).toFixed(2),
                        "banRate": (championStatsObject.globalBanRate*100).toFixed(2),
                        "pickOrder": championStatsObject.mostPopularPickOrder
                    }
                    championListTemp.push(tempDict)
                }
                return championListTemp
                
            }).then(list => {
                newChampionList.push(list.slice(0, 6))
                setChampionList(newChampionList)
            })
        }
        setFlagDisplay(true)
    }

    useEffect(() => {
        fetchTopMetaPicks()
    }, [])

    return (
        
        <div className="champion-overview">
            <p>{championList.length}</p>
            {
                (flagDisplay && championList.length > 4) &&
                <>
                    <div className="champion-overview-content">
                        <h2>Toplane</h2>
                        <ul className="champion-overview-list">
                            {   
                                championList[0].map((championStats) =>
                                    <li>
                                        <ChampionIcon
                                            championName={championStats.championName}
                                            winRate={championStats.winRate}
                                            pickRate={championStats.pickRate}
                                            banRate={championStats.banRate}
                                            pickOrder={championStats.pickOrder}
                                        />
                                    </li> 
                                )
                            }
                        </ul>
                    </div>
                    
                    <div className="champion-overview-content">
                        <h2>Jungle</h2>
                        <ul className="champion-overview-list">
                            {
                                championList[1].map((championStats) =>
                                    <li>
                                        <ChampionIcon
                                            championName={championStats.championName}
                                            winRate={championStats.winRate}
                                            pickRate={championStats.pickRate}
                                            banRate={championStats.banRate}
                                            pickOrder={championStats.pickOrder}
                                        />
                                    </li> 
                                )
                            }
                        </ul>
                    </div>
                    
                    <div className="champion-overview-content">
                        <h2>Midlane</h2>
                        <ul className="champion-overview-list">
                            {
                                championList[2].map((championStats) =>
                                    <li>
                                        <ChampionIcon
                                            championName={championStats.championName}
                                            winRate={championStats.winRate}
                                            pickRate={championStats.pickRate}
                                            banRate={championStats.banRate}
                                            pickOrder={championStats.pickOrder}
                                        />
                                    </li> 
                                )
                            }
                        </ul>
                    </div>
                    
                    <div className="champion-overview-content">
                        <h2>ADC</h2>
                        <ul className="champion-overview-list">
                            {
                                championList[3].map((championStats) =>
                                    <li>
                                        <ChampionIcon
                                            championName={championStats.championName}
                                            winRate={championStats.winRate}
                                            pickRate={championStats.pickRate}
                                            banRate={championStats.banRate}
                                            pickOrder={championStats.pickOrder}
                                        />
                                    </li> 
                                )
                            }
                        </ul>
                    </div>
                    
                    <div className="champion-overview-content">
                        <h2>Support</h2>
                        <ul className="champion-overview-list">
                            {
                                championList[4].map((championStats) =>
                                    <li>
                                        <ChampionIcon
                                            championName={championStats.championName}
                                            winRate={championStats.winRate}
                                            pickRate={championStats.pickRate}
                                            banRate={championStats.banRate}
                                            pickOrder={championStats.pickOrder}
                                        />
                                    </li> 
                                )
                            }
                        </ul>
                    </div>
                </>
            }
        </div>
    )
}