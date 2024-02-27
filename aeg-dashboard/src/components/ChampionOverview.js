import NavBarComp from "./NavbarComp";
import SelectComp from "./SelectComp";
import "../styles/ChampionOverview.css"

function ChampionOverview() {
    const patchList = [1.4, 1.14];
    const side = ["Blue", "Red", "Both"]
    const tournamentList = ["Tournament 1", "Tournament 2"]
    // TODO: Make an API call to backend to get the list of Patches and Tournaments available
    return(
        <div>
            <NavBarComp />
            <h1>Champion Overview</h1>
            <div className="dashboard-champOverview-controlPannel">
                <ul className="dashboard-champOverview-controlPannel-list">
                    <li>
                        <SelectComp elementList={patchList} defaultValue={"--Patch--"}/>
                    </li>
                    <li>
                        <SelectComp elementList={side} defaultValue={"--Side--"} />
                    </li>
                    <li>
                        <SelectComp elementList={tournamentList} defaultValue={"--Tournament--"} />
                    </li>
                </ul>
            </div>
        </div>
     
    )
}

export default ChampionOverview