import SelectComp from "./SelectComp";
import ChampionIcon from "./ChampionIcon";
import { useState } from "react";

function TopMetaPicksPanel(props) {
    const [activePatch, setActivePatch] = useState('Select a patch')
    const [activeSide, setActiveSide] = useState('Select a side')
    const [activeTournament, setActiveTournament] = useState("Select a tournament")
    const [activeFilter, setActiveFilter] = useState("Select a filter")

    const {value, panelIndex} = props
    const patchList = [1.4, 1.14];
    const side = ["Blue", "Red", "Both"];
    const tournamentList = ["Tournament 1", "Tournament 2"];
    const filterList = ["WinRate", "PickRate", "BanRate", "PickOrder"]

    const championListToplane = ["Aatrox", "Renekton", "KSante", "Fiora", "Gragas", "Jax"];
    const championListJungle = ["Maokai", "Viego", "Lillia", "LeeSin", "Volibear", "Belveth"];
    const championListMidlane = ["Azir", "Tristana", "Hwei", "TwistedFate", "Ahri", "Taliyah"];
    const championListADC = ["Smolder", "Varus", "Senna", "Kalista", "Ezreal", "Kaisa"];
    const championListSupport = ["Nautilus", "Leona", "Thresh", "Rakan", "Alistar", "Blitzcrank"]
    return (
        <div
            role='tabpanbel'
            hidden={value !== panelIndex}
            className={`simple-tabpanel-${panelIndex}`}
            aria-labelledby={`simple-tab-${panelIndex}`}
        >
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

            <div className="sorter">
                <ul>
                    <li>Sort by</li>
                    <li>
                    <SelectComp 
                        elementList={filterList}
                        defaultValue={"-- Select Filter --"}
                        setActive={setActiveFilter}
                    />
                    </li>
                </ul>                
            </div>

            <div className="champion-overview">
                <div className="champion-overview-content">
                    <h2>Toplane</h2>
                    <ul className="champion-overview-list">
                        {championListToplane.map((championName) =>
                            <li>
                                <ChampionIcon
                                    championName={championName}
                                    winRate={50}
                                    pickRate={60}
                                    banRate={30}
                                    pickOrder={1}
                                />
                            </li> 
                        )}
                    </ul>
                </div>
                

                <div className="champion-overview-content">
                    <h2>Jungle</h2>
                    <ul className="champion-overview-list">
                        {championListJungle.map((championName) => 
                            <li>
                                <ChampionIcon
                                    championName={championName}
                                    winRate={50}
                                    pickRate={60}
                                    banRate={30}
                                    pickOrder={1}
                                />
                            </li> 
                        )}
                    </ul>
                </div>
                
                <div className="champion-overview-content">
                    <h2>Midlane</h2>
                    <ul className="champion-overview-list">
                        {championListMidlane.map((championName) => 
                            <li>
                                <ChampionIcon
                                    championName={championName}
                                    winRate={50}
                                    pickRate={60}
                                    banRate={30}
                                    pickOrder={1}
                                />
                            </li> 
                        )}
                    </ul>
                </div>
                
                <div className="champion-overview-content">
                    <h2>ADC</h2>
                    <ul className="champion-overview-list">
                        {championListADC.map((championName) => 
                            <li>
                                <ChampionIcon
                                    championName={championName}
                                    winRate={50}
                                    pickRate={60}
                                    banRate={30}
                                    pickOrder={1}
                                />
                            </li> 
                        )}
                    </ul>
                </div>
                
                <div className="champion-overview-content">
                    <h2>Support</h2>
                    <ul className="champion-overview-list">
                        {championListSupport.map((championName) => 
                            <li>
                                <ChampionIcon
                                    championName={championName}
                                    winRate={50}
                                    pickRate={60}
                                    banRate={30}
                                    pickOrder={1}
                                />
                            </li> 
                        )}
                    </ul>
                </div>
            </div>
        </div>

    )
}

export default TopMetaPicksPanel;