import NavBarComp from "./utils/NavbarComp"
import "../styles/TestComp.css"

import { Typography } from "@mui/material"

import { useState, useEffect, useContext } from "react"
import { API_URL } from "../constants"
import AuthContext from "./context/AuthContext"
import DraftGrid from "./utils/DraftGrid"



function TestComp() {
    const [rows, setRows] = useState([])

    let {authTokens} = useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }

    useEffect(() => {
        const fetchChampionsDraftStats = async (teamName, tournamentList, side) => {
            const data = {
                "teamName": teamName,
                "tournamentList": tournamentList,
                "side": side
            }
            const result = await fetch(API_URL + `teamAnalysis/getDraftStats/`, {
                method: "PATCH",
                headers: header,
                body: JSON.stringify(data)
            })
            result.json().then(result => {
                const newData = result;
                let newRows = newData.map(({ pk, championName, patch, side, mostPopularRole, mostPopularPickOrder, tournament, ...rest }) => {
                    let updatedFields = Object.fromEntries(
                        Object.entries(rest).map(([key, value]) => [key, parseFloat((value * 100).toFixed(2))])
                    );

                    return {
                        id: pk,
                        championName,
                        mostPopularRole,
                        ...updatedFields
                    };
                });
                setRows(newRows)
            })
        }
        fetchChampionsDraftStats("FNC", ["LEC - Winter 2025 (Regular Season: Regular Season)"], "Both")
    }, [])
    


    return (
        <div className="wrapper-Test">
            <NavBarComp/>
            <Typography id="title-Test" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold", mb: 10}}>
                Test page
            </Typography>
            <DraftGrid rows={rows}/>
            
        </div>
    )
}

export default TestComp