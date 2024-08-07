import { useEffect, useState, useContext } from "react";
import DraftComponent from "../utils/DraftComponent";
import { API_URL } from "../../constants";
import AuthContext from "../context/AuthContext";

function LatestDraftsPanel(props) {
    const {value, panelIndex} = props
    const [patch, setPatch] = useState("")
    const [draftList, setActiveDraftList] = useState([])

    let {authTokens} = useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }
    useEffect(() => {
        async function fetchLatestDrafts() {
            const result = await fetch(API_URL + "draft/getLatest/5/1/", {
                method: "GET",
                headers: header
            })
            result.json().then(result => {
                const newDraftList = result;
                setActiveDraftList(newDraftList)
                let temp = newDraftList[0].patch
                const newPatch = temp.split(".")[0] + "." + temp.split(".")[1] + ".1"
                setPatch(newPatch)
            })
        }

        fetchLatestDrafts();
    }, [])


    return (
        <div
            role='tabpanbel'
            hidden={value !== panelIndex}
            className={`simple-tabpanel-${panelIndex}`}
            aria-labelledby={`simple-tab-${panelIndex}`}
        >
            {
                draftList.map((draftObject) => 
                    <DraftComponent
                        team1Name={draftObject.teamBlue}
                        team2Name={draftObject.teamRed}
                        picksB1rota={[draftObject.bp1, draftObject.bp2, draftObject.bp3]}
                        picksB2rota={[draftObject.bp4, draftObject.bp5]}
                        picksR1rota={[draftObject.rp1, draftObject.rp2, draftObject.rp3]}
                        picksR2rota={[draftObject.rp4, draftObject.rp5]}
                        bansB1rota={[draftObject.bb1, draftObject.bb2, draftObject.bb3]}
                        bansB2rota={[draftObject.bb4, draftObject.bb5]}
                        bansR1rota={[draftObject.rb1, draftObject.rb2, draftObject.rb3]}
                        bansR2rota={[draftObject.rb4, draftObject.rb5]}
                        win={draftObject.winner}
                        patch={patch}
                    />
                )
            }        
            <br/>
        </div>
        
    )
}

export default LatestDraftsPanel;