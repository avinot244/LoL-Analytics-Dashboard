import NavBarComp from "./NavbarComp";
import SelectComp from "./SelectComp";
import "../styles/ChampionOverview.css"
import { useState } from "react";

function ChampionOverview() {
    const patchList = [1.4, 1.14];
    const side = ["Blue", "Red", "Both"]
    const tournamentList = ["Tournament 1", "Tournament 2"]

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

            <p>Selected patch : {activePatch}</p>
            <p>Selected side : {activeSide}</p>
            <p>Selected Tournament : {activeTournament}</p>
            
        
        </div>
     
    )
}


export default ChampionOverview