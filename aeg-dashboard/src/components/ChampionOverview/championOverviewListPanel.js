import { API_URL } from "../../constants/index";
import ChampionIcon from "../utils/ChampionIcon";
import { useState, useEffect, useContext } from "react";
import Loading from "../utils/Loading";
import AuthContext from "../context/AuthContext";

export default function ChampionOverviewListPanel(props) {
    const {filter, side, patch, tournament} = props


    const [topPicksTop, setTopPicksTop] = useState([])
    const [topPicksJungle, setTopPicksJungle] = useState([])
    const [topPicksMid, setTopPicksMid] = useState([])
    const [topPicksADC, setTopPicksADC] = useState([])
    const [topPicksSupport, setTopPicksSupport] = useState([])

    const [loading, setLoading] = useState(true);
    let {authTokens} = useContext(AuthContext)


    const fetchTopMetaPicks = async () => {
        const header = {
            Authorization: "Bearer " + authTokens.access
        }
        const resultTop = await fetch(API_URL + `draft/championStats/getTopChampions/Top/${filter}/${side}/${patch}/${tournament}/`, {
            method: "GET",
            headers:header
        })
        let newTopPicksTop = []
        resultTop.json().then(result => {
            for (let i = 0 ; i < result.length ; i++) {
                let championStatsObject = result[i]
                let tempDict = {
                    "championName": championStatsObject.championName,
                    "winRate": (championStatsObject.winRate*100).toFixed(2),
                    "pickRate": (championStatsObject.globalPickRate*100).toFixed(2),
                    "banRate": (championStatsObject.globalBanRate*100).toFixed(2),
                    "pickOrder": championStatsObject.mostPopularPickOrder
                }
                newTopPicksTop.push(tempDict)
            }
            return newTopPicksTop
        }).then(list => {
            let temp = list.slice(0, 6)
            setTopPicksTop(temp)
        })

        const resultJungle = await fetch(API_URL + `draft/championStats/getTopChampions/Jungle/${filter}/${side}/${patch}/${tournament}/`, {
            method: "GET",
            headers:header
        })
        let newTopPicksJungle = []
        resultJungle.json().then(result => {
            for (let i = 0 ; i < result.length ; i++) {
                let championStatsObject = result[i]
                let tempDict = {
                    "championName": championStatsObject.championName,
                    "winRate": (championStatsObject.winRate*100).toFixed(2),
                    "pickRate": (championStatsObject.globalPickRate*100).toFixed(2),
                    "banRate": (championStatsObject.globalBanRate*100).toFixed(2),
                    "pickOrder": championStatsObject.mostPopularPickOrder
                }
                newTopPicksJungle.push(tempDict)
            }
            return newTopPicksJungle
        }).then(list => {
            let temp = list.slice(0, 6)
            setTopPicksJungle(temp)
        })

        const resultMid = await fetch(API_URL + `draft/championStats/getTopChampions/Mid/${filter}/${side}/${patch}/${tournament}/`, {
            method: "GET",
            headers:header
        })
        let newTopPicksMid = []
        resultMid.json().then(result => {
            for (let i = 0 ; i < result.length ; i++) {
                let championStatsObject = result[i]
                let tempDict = {
                    "championName": championStatsObject.championName,
                    "winRate": (championStatsObject.winRate*100).toFixed(2),
                    "pickRate": (championStatsObject.globalPickRate*100).toFixed(2),
                    "banRate": (championStatsObject.globalBanRate*100).toFixed(2),
                    "pickOrder": championStatsObject.mostPopularPickOrder
                }
                newTopPicksMid.push(tempDict)
            }
            return newTopPicksMid
        }).then(list => {
            let temp = list.slice(0, 6)
            setTopPicksMid(temp)
        })

        const resultADC = await fetch(API_URL + `draft/championStats/getTopChampions/ADC/${filter}/${side}/${patch}/${tournament}/`, {
            method: "GET",
            headers:header
        })
        let newTopPicksADC = []
        resultADC.json().then(result => {
            for (let i = 0 ; i < result.length ; i++) {
                let championStatsObject = result[i]
                let tempDict = {
                    "championName": championStatsObject.championName,
                    "winRate": (championStatsObject.winRate*100).toFixed(2),
                    "pickRate": (championStatsObject.globalPickRate*100).toFixed(2),
                    "banRate": (championStatsObject.globalBanRate*100).toFixed(2),
                    "pickOrder": championStatsObject.mostPopularPickOrder
                }
                newTopPicksADC.push(tempDict)
            }
            return newTopPicksADC
        }).then(list => {
            let temp = list.slice(0, 6)
            setTopPicksADC(temp)
        })

        const resultSupport = await fetch(API_URL + `draft/championStats/getTopChampions/Support/${filter}/${side}/${patch}/${tournament}/`, {
            method: "GET",
            headers:header
        })
        let newTopPicksSupport = []
        resultSupport.json().then(result => {
            for (let i = 0 ; i < result.length ; i++) {
                let championStatsObject = result[i]
                let tempDict = {
                    "championName": championStatsObject.championName,
                    "winRate": (championStatsObject.winRate*100).toFixed(2),
                    "pickRate": (championStatsObject.globalPickRate*100).toFixed(2),
                    "banRate": (championStatsObject.globalBanRate*100).toFixed(2),
                    "pickOrder": championStatsObject.mostPopularPickOrder
                }
                newTopPicksSupport.push(tempDict)
            }
            return newTopPicksSupport
        }).then(list => {
            let temp = list.slice(0, 6)
            setTopPicksSupport(temp)
        })

    }

    useEffect(() => {
        fetchTopMetaPicks()
        setLoading(false)
    }, [])

    return (
        
        <div className="champion-overview">
            {
                loading ? (
                    <Loading />
                ) : (
                    <>
                        <div className="champion-overview-content">
                            <h2>Toplane</h2>
                            <ul className="champion-overview-list">
                                {   
                                    topPicksTop.map((championStats) =>
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
                                    topPicksJungle.map((championStats) =>
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
                                    topPicksMid.map((championStats) =>
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
                                    topPicksADC.map((championStats) =>
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
                                    topPicksSupport.map((championStats) =>
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
                )
            }
        </div>
    )
}