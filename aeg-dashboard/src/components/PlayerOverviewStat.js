import "../styles/PlayerOverviewStat.css"
import ChampionIcon from "./ChampionIcon";
import { API_URL, behaviorModelUUID } from "../constants";
import { useEffect, useState } from "react";

export default function PlayerOverviewStat(props) {
    const {role, summonnerName, patch, wantedTournament, limit} = props

    const [behaviorPatch, setBehaviorPatch] = useState()
    const [behaviorLatest, setBehaviorLatest] = useState()

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
                setBehaviorPatch(newBehaviorPatch)
                console.log(behaviorPatch)
            })
        }

        const fetchBehaviorTournamentLatestPlayer = async (role, summonnerName, limit, wantedTournament) => {
            const result = await fetch(API_URL + `behavior/${role}/compute/${summonnerName}/${limit}/${behaviorModelUUID}/${wantedTournament}/${wantedTournament}/`, {
                method: "GET"
            })
            result.json().then(result => {
                const newBehaviorLatest = result
                setBehaviorLatest(newBehaviorLatest)
                console.log(behaviorLatest)
            })
        }
        fetchBehaviorTournamentPatchPlayer(role, summonnerName, patch, wantedTournament)
        fetchBehaviorTournamentLatestPlayer(role, summonnerName, limit, wantedTournament)

    }, [])

    

    return (
        <div className="playerOverview-content-wrapper">
            <div className="playerOverview-graph">
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