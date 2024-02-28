import NavBarComp from "./NavbarComp";
import SelectComp from "./SelectComp";
import "../styles/ChampionOverview.css"
import { useState } from "react";
import ChampionIcon from "./ChampionIcon";

function ChampionOverview() {
    const patchList = [1.4, 1.14];
    const side = ["Blue", "Red", "Both"];
    const tournamentList = ["Tournament 1", "Tournament 2"];

    const championListToplane = ["Aatrox", "Renekton", "KSante"];
    const championListJungle = ["Maokai", "Viego", "Lillia"];
    const championListMidlane = ["Azir", "Tristana", "Hwei"];
    const championListADC = ["Smolder", "Varus", "Senna"];
    const championListSupport = ["Nautilus", "Leona", "Thresh"]

    const [activePatch, setActivePatch] = useState('Select a patch')
    const [activeSide, setActiveSide] = useState('Select a side')
    const [activeTournament, setActiveTournament] = useState("Select a tournament")

    // TODO: Make an API call to backend to get the list of Patches and Tournaments available
    return(
        <div className="wrapper-overview">
            <NavBarComp />
            <h1>Champion Overview</h1>
            <div className="dashboard-champOverview-controlPannel">
                <ul className="dashboard-champOverview-controlPannel-list">
                    <li>
                        <SelectComp 
                            elementList={patchList}
                            defaultValue={"-- Patch --"}
                            setActive={setActivePatch}/>
                    </li>
                    <li>
                        <SelectComp
                            elementList={side}
                            defaultValue={"-- Side --"}
                            setActive={setActiveSide}/>
                    </li>
                    <li>
                        <SelectComp 
                            elementList={tournamentList}
                            defaultValue={"-- Tournament --"}
                            setActive={setActiveTournament}/>
                    </li>
                </ul>
            </div>

            <br/>

            <div className="champion-overview-content">
                <div className="champion-overview-content-toplane">
                    <h2>Toplane</h2>
                    <ul className="champion-overview-list">
                        {championListToplane.map((championName) => 
                            <ChampionIcon
                                championName={championName}
                                winRate={50}
                                pickRate={60}
                            />
                        )}
                    </ul>
                </div>
                
                <div className="champion-overview-content-jungle">
                    <h2>Jungle</h2>
                    <ul className="champion-overview-list">
                        {championListJungle.map((championName) => 
                            <ChampionIcon
                                championName={championName}
                                winRate={50}
                                pickRate={60}
                            />
                        )}
                    </ul>
                </div>
                
                <div className="champion-overview-content-midlane">
                    <h2>Midlane</h2>
                    <ul className="champion-overview-list">
                        {championListMidlane.map((championName) => 
                            <ChampionIcon
                                championName={championName}
                                winRate={50}
                                pickRate={60}
                            />
                        )}
                    </ul>
                </div>
                
                <div className="champion-overview-content-adc">
                    <h2>ADC</h2>
                    <ul className="champion-overview-list">
                        {championListADC.map((championName) => 
                            <ChampionIcon
                                championName={championName}
                                winRate={50}
                                pickRate={60}
                            />
                        )}
                    </ul>
                </div>
                
                <div className="champion-overview-content-support">
                    <h2>Support</h2>
                    <ul className="champion-overview-list">
                        {championListSupport.map((championName) => 
                            <ChampionIcon
                                championName={championName}
                                winRate={50}
                                pickRate={60}
                            />
                        )}
                    </ul>
                </div>
            </div>
        </div>    
    )
}


export default ChampionOverview