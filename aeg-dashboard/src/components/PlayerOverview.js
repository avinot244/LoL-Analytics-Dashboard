import NavBarComp from "./NavbarComp"
import "../styles/PlayerOverview.css"
import SelectComp from "./SelectComp";
import { useState } from "react";
import ChampionIcon from "./ChampionIcon";
import PlayerSelectComp from "./PlayerSelectComp"

function PlayerOverview(){
    const patchList = [1.4, 1.14, 1.3];
    const weekList = ["Week 1", "Week 2", "Week 3"]

    const championList = ["Hwei", "Thresh", "Leona", "Maokai", "Senna", "Nautilus"]

    const [activePatch, setActivePatch] = useState('Select a patch')
    const [activeWeek,  setActiveWeek] = useState('Select a week')
    const [selectedPlayer, setSelectedPlayer] = useState('Select a player')

    return(
        
        <div className="wrapper-overview-player">
            <NavBarComp />
            <h1> Player Overview </h1>
            <div className="dashboard-playerOverview-controlPannel">
                <ul className="dashboard-playerOverview-controlPannel-list">
                    <li>
                        <SelectComp 
                            elementList={weekList}
                            defaultValue={"-- Week --"}
                            setActive={setActiveWeek}/>
                    </li>
                    <li>
                        <SelectComp
                            elementList={patchList}
                            defaultValue={"-- Patch --"}
                            setActive={setActivePatch}/>
                    </li>
                </ul>
            </div>

            <br/>
            <div className="playerOverview-playerSelect">
                <PlayerSelectComp
                    selectedPlayer={selectedPlayer}
                    setSelectedPlayer={setSelectedPlayer}
                />
                <p>Selected player :</p>
                <p>{selectedPlayer}</p>
            </div>
            

            <br/>

            <div className="playerOverview-content-wrapper">
                <div className="playerOverview-graph">

                </div>
                <div className="playerOverview-other-content">
                    <div className="playerOverview-stats">

                    </div>
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
        </div>
    )
}

export default PlayerOverview