import NavBarComp from "./utils/NavbarComp"
import "../styles/TestComp.css"
import AuthContext from "./context/AuthContext"
import ChampionIconSmall from "./utils/ChampionIconSmall"
import GradientTypographyReverted from "./utils/GradientTypographyReverted"

import { Typography, Button, Stack, Paper } from "@mui/material"
import { DataGrid } from '@mui/x-data-grid';
import { useDemoData } from '@mui/x-data-grid-generator';

import { useState, useEffect, useContext, useRef } from "react"
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

function TestComp() {
    // const [rows, setRows] = useState([])
    // const [columns, setColumns] = useState([])

    const columns = [
        {
            field: 'championName',
            headerName: 'Champion',
            width: 75,
            renderCell: RenderChampion
        },
        {
            field: 'winRate',
            headerName: 'Win Rate',
            width: 150,
            renderCell: RenderDraftData
        }
    ]
    const rows = [
        {
            id: 1,
            championName: "Aatrox",
            winRate: 67.778
        }
    ]


    return (
        <div className="wrapper-Test">
            <NavBarComp/>
            <Typography id="title-Test" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold", mb: 10}}>
                Test page
            </Typography>

            <Paper sx={{ height: 520, width: '100%' }}>
                <DataGrid
                    rows={rows}
                    columns={columns}
                    rowHeight={38}
                    checkboxSelection
                    disableRowSelectionOnClick
                />
            </Paper>
        </div>
    )
}

export default TestComp