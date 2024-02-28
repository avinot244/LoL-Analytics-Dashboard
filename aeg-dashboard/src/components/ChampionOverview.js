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
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut suscipit consectetur orci vitae posuere. Proin nunc massa, mollis in quam et, pharetra convallis leo. Nulla quis mauris nisi. Duis elementum odio non dapibus tempus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Maecenas rhoncus eros nec libero fringilla ultrices. Donec fringilla suscipit sagittis. Nullam aliquet, turpis eu scelerisque vestibulum, ante massa vehicula felis, sed congue erat mauris condimentum turpis. </p>
            <p>Quisque sed mollis mauris. Sed dictum malesuada urna ac vehicula. Pellentesque vitae volutpat felis. Maecenas accumsan iaculis lacus vitae mollis. Quisque elit orci, vehicula vitae auctor sed, gravida a odio. Aliquam nibh mi, egestas nec risus ut, egestas sodales nunc. Mauris ut mollis mauris, in iaculis urna. Quisque ultricies semper lorem ac dictum. Vivamus at felis non nisl hendrerit tincidunt in id urna. </p>
            <p>Donec fringilla vestibulum rutrum. Fusce convallis ac sapien lobortis blandit. Praesent finibus erat et felis posuere, at lacinia velit ullamcorper. Sed eu mauris vel ex porta commodo ut consectetur felis. Donec cursus diam ac pellentesque ullamcorper. Quisque egestas ultrices tortor, eu hendrerit lectus accumsan id. Morbi ullamcorper vehicula massa ac rutrum. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Proin at sollicitudin metus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Quisque iaculis tortor at accumsan pretium. </p>
            <p>Nam nunc augue, tempus ut ornare a, consectetur nec turpis. Duis vitae tellus quis nibh pulvinar pharetra eget nec est. Donec augue augue, fermentum a quam non, lobortis semper leo. Phasellus nunc magna, malesuada id condimentum sed, mollis quis tellus. Donec auctor dui turpis, vel sodales lorem rhoncus et. Quisque in felis eu libero rutrum dapibus eu id ipsum. Nam sit amet neque at odio suscipit porta. Ut quis libero sed urna laoreet aliquam. Ut tincidunt eu nisi a interdum. Donec id finibus massa. </p>
            <p>Phasellus et ornare lectus. Proin sit amet vehicula tellus. Etiam bibendum est pulvinar, ullamcorper lacus vitae, placerat ex. Vivamus placerat libero molestie quam scelerisque, eu ornare augue vestibulum. Suspendisse ac tellus quis tellus euismod lacinia a id mauris. Donec consectetur ante ut dui finibus porta. Pellentesque accumsan nisl et interdum ornare. Sed at maximus felis. Vivamus vitae urna vitae risus euismod ornare. Maecenas sem leo, venenatis eget condimentum non, aliquet a mauris. Sed pulvinar, ipsum eget tincidunt iaculis, sapien ante ullamcorper eros, a ullamcorper libero nibh a ante. Nulla semper eros neque, ut sagittis ante rhoncus ut. </p>
        
        </div>
     
    )
}


export default ChampionOverview