import NavBarComp from "./NavbarComp"
import "../styles/PlayerOverview.css"
import SelectComp from "./SelectComp";
import { useState } from "react";
import ChampionIcon from "./ChampionIcon";
import SearchComp from "./SearchComp"

function PlayerOverview(){
    const patchList = [1.4, 1.14, 1.3];
    const weekList = ["Week 1", "Week 2", "Week 3"]

    const championList = ["Hwei", "Thresh", "Leona", "Maokai", "Senna", "Nautilus"]

    const [activePatch, setActivePatch] = useState('Select a patch')
    const [activeWeek,  setActiveWeek] = useState('Select a week')
    const [selectedPlayer, setSelectedPlayer] = useState('Select a player')

    const playerList = [
		{value: 'aeg_agresivoo', label: "AEG Agresivoo"},
		{value: "aeg_ryuzaki", label: "AEG Ryuzaki"},
		{value: "aeg_nafkelah", label: "AEG Nafkelah"},
		{value: "aeg_hid0", label: "AEG Hid0"},
		{value: "aeg_veignorem", label: "AEG Veignorem"},
		{value: "g2_broken_blade", label: "G2 Broken Blade"},
		{value: "g2_yike", label: "G2 Yike"},
		{value: "g2_caps", label: "G2 Caps"},
		{value: "g2_hans_sama", label: "G2 Hans Sama"},
		{value: "g2_mikyx", label: "G2 Mikyx"}
	]

    const gd15 = 450
    const k15 = 4
    const d15 = 1
    const a15 = 5

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
                <SearchComp
                    selectedElement={selectedPlayer}
                    setSelectedElement={setSelectedPlayer}
                    elementList={playerList}
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
        </div>
    )
}

export default PlayerOverview