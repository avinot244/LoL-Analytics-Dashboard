import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';

import AuthContext from '../context/AuthContext';

const columns = [
    { field: 'playerName', headerName: 'Player Name', width: 130 },
    { field: 'aggressive', headerName: 'Agressive', width: 130 },
    { field: 'farming_safely', headerName: 'Farming Safely', width: 130 },
    { field: 'objectives_towers', headerName: 'Objectives/Tower', width: 130 },
    { field: 'playing_alone', headerName: 'Playing Alone', width: 130 },
    { field: 'invader', headerName: 'Invader', width: 130 },
];

let rows = []
for (let i = 0 ; i < 10; i++) {
    rows.push({
        id: i,
        playerName: i,
        aggressive: Math.random().toFixed(2),
        farming_safely: Math.random().toFixed(2),
        objectives_towers: Math.random().toFixed(2),
        playing_alone: Math.random().toFixed(2),
        invader: Math.random().toFixed(2)
    })
}
const paginationModel = { page: 0, pageSize: 5 };

export default function PlayerScoutingTop(props){
    const {value, panelIndex} = props

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
                    <Paper sx={{ height: 400, width: '100%' }}>
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