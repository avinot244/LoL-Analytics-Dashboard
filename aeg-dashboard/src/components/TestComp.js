import NavBarComp from "./utils/NavbarComp"
import "../styles/TestComp.css"
import AuthContext from "./context/AuthContext"
import ChampionIconSmall from "./utils/ChampionIconSmall"
import GradientTypographyReverted from "./utils/GradientTypographyReverted"

import { Typography, Button, Stack, Paper } from "@mui/material"
import { DataGrid } from '@mui/x-data-grid';
import { useDemoData } from '@mui/x-data-grid-generator';

import { useState, useEffect, useContext } from "react"
import { API_URL } from "../constants"


function RenderChampion(props){
    const {_, value} = props
    return (
        <ChampionIconSmall championName={value} width={50} height={50}/>
    )
}

function RenderDraftData(props) {
    const {_, value} = props
    return (
        <GradientTypographyReverted value={value} bold>{value}%</GradientTypographyReverted>
    )
}

function camelCaseToTitle(str) {
    return str
        .replace(/([A-Z])/g, ' $1') // Insert space before capital letters
        .replace(/^./, match => match.toUpperCase()); // Capitalize the first letter
}

function TestComp() {
    const [rows, setRows] = useState([])
    // const [columns, setColumns] = useState([])

    const columns = [
        {
            field: 'championName',
            headerName: 'Champion',
            width: 150,
            renderCell: RenderChampion
        },
        {
            field: 'winRate',
            headerName: 'Win Rate',
            width: 150,
            renderCell: RenderDraftData
        },
        {
            field: 'draftPresence',
            headerName: 'Draft Presence',
            width: 150,
            renderCell: RenderDraftData
        },
        {
            field: 'globalPickRate',
            headerName: 'Global Pick Rate',
            width: 150,
            renderCell: RenderDraftData
        },
        {
            field: 'pickRate1Rota',
            headerName: 'Pick Rate 1st Rotation',
            width: 150,
            renderCell: RenderDraftData
        },
        {
            field: 'pickRate2Rota',
            headerName: 'Pick Rate 2nd Rotation',
            width: 150,
            renderCell: RenderDraftData
        },
        {
            field: 'globalBanRate',
            headerName: 'Global Ban Rate',
            width: 150,
            renderCell: RenderDraftData
        },
        {
            field: 'banRate1Rota',
            headerName: 'Ban Rate 1st Rotation',
            width: 150,
            renderCell: RenderDraftData
        },
        {
            field: 'banRate2Rota',
            headerName: 'Ban Rate 2nd Rotationi',
            width: 150,
            renderCell: RenderDraftData
        },
        {
            field: 'blindPick',
            headerName: 'Blind Pick',
            width: 150,
            renderCell: RenderDraftData
        }
    ]

    let {authTokens} = useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }

    const paginationModel = { page: 0, pageSize: 5 };

    useEffect(() => {
        const fetchChampionsDraftStats = async (tournament, patch, side) => {
            const result = await fetch(API_URL + `draft/championStats/getStats/${patch}/${side}/${tournament}/`, {
                method: "GET",
                headers:header
            })
            result.json().then(result => {
                const newData = result;
                let newRows = newData.map(({ pk, championName, patch, side, mostPopularRole, mostPopularPickOrder, tournament, ...rest }) => {
                    let updatedFields = Object.fromEntries(
                        Object.entries(rest).map(([key, value]) => [key, (value * 100).toFixed(2)])
                    );
                
                    return {
                        id: pk,
                        championName,
                        ...updatedFields
                    };
                });
                setRows(newRows)
                console.log(newRows)
            })
        }
        
        fetchChampionsDraftStats("LEC - Winter 2025 (Regular Season: Regular Season)", "15.2", "Blue")
    }, [])
    


    return (
        <div className="wrapper-Test">
            <NavBarComp/>
            <Typography id="title-Test" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold", mb: 10}}>
                Test page
            </Typography>

            <Paper sx={{ height: 370, width: '100%' }}>
                <DataGrid
                   rows={rows}
                   columns={columns}
                   initialState={{ pagination: { paginationModel } }}
                   pageSizeOptions={[5, 10]}
                   checkboxSelection
                   sx={{ border: 0 }}
                    
                />
            </Paper>
        </div>
    )
}

export default TestComp