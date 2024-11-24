import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import { useDemoData } from '@mui/x-data-grid-generator';

import AuthContext from '../context/AuthContext';
import GradientTypography from '../utils/GradientTypography';

const columns_bis = [
    { field: 'playerName', headerName: 'Player Name', width: 130 },
    { field: 'aggressive', headerName: 'Agressive', width: 130 },
    { field: 'farming_safely', headerName: 'Farming Safely', width: 130 },
    { field: 'objectives_towers', headerName: 'Objectives/Towers', width: 130 },
    { field: 'playing_alone', headerName: 'Playing Alone', width: 130 },
    { field: 'invader', headerName: 'Invader', width: 130 },
];

function RenderData(props) {
    const {_, value} = props
    return (
        <GradientTypography value={value} bold>{value}%</GradientTypography>
    )
}

const columns = [
    {
        field: 'playerName',
        headerName: 'Player Name', 
        width: 130
    },
    {
        field: 'region',
        headerName: 'Region', 
        width: 130
    },
    {
        field: 'aggressive',
        headerName: 'Aggressive',
        renderCell: RenderData,
        width: 130
    },
    {
        field: 'farming_safely',
        headerName: 'Farming Safely',
        renderCell: RenderData,
        width: 130
    },
    {
        field: 'objectives_towers',
        headerName: 'Objectives/Towers',
        renderCell: RenderData,
        width: 150
    },
    {
        field: 'playing_alone',
        headerName: 'Playing Alone',
        renderCell: RenderData,
        width: 130
    },
    {
        field: 'invader',
        headerName: 'Invader',
        renderCell: RenderData,
        width: 130
    },
]


let rows = []
for (let i = 0 ; i < 10; i++) {
    rows.push({
        id: i,
        playerName: i,
        region: i+i,
        aggressive: (Math.random()*100).toFixed(2),
        farming_safely: (Math.random()*100).toFixed(2),
        objectives_towers: (Math.random()*100).toFixed(2),
        playing_alone: (Math.random()*100).toFixed(2),
        invader: (Math.random()*100).toFixed(2)
    })
}
const paginationModel = { page: 0, pageSize: 5 };

export default function PlayerScoutingTop(props){
    const {value, panelIndex} = props

    const { data, loading } = useDemoData({
        dataSet: 'Commodity',
        rowLength: 10,
        editable: true,
    });

    console.log(data)

    let {authTokens} = React.useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }

    return (
        <div className="wrapper-player-scouting-Top">
            <div
                role='tabpanbel'
                hidden={value !== panelIndex}
                className={`simple-tabpanel-${panelIndex}`}
                aria-labelledby={`simple-tab-${panelIndex}`}
            >
                {
                    panelIndex === 0 &&
                    <Paper sx={{ height: 400, width: '100%', marginTop: '15px'}}>
                        <DataGrid
                            rows={rows}
                            columns={columns}
                            initialState={{ pagination: { paginationModel } }}
                            pageSizeOptions={[5, 10]}
                            checkboxSelection
                            sx={{ border: 0 }}
                        />
                    </Paper>

                }
            </div>
        </div>
    )
}