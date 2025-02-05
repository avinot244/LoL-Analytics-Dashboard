import ChampionIconSmall from "./ChampionIconSmall"
import GradientTypographyReverted from "./GradientTypographyReverted"

import { Paper } from "@mui/material"
import { DataGrid } from '@mui/x-data-grid';

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

function RenderStr(props) {
    const {_, value} = props
    return (
        <span>{value}</span>
    )
}

function DraftGrid({ rows }) {
    const columns = [
        {
            field: 'championName',
            headerName: 'Champion',
            width: 150,
            renderCell: RenderChampion
        },
        {
            field: 'mostPopularRole',
            headerName: "Role",
            width: 100,
            renderCell: RenderStr
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
            width: 160,
            renderCell: RenderDraftData
        },
        {
            field: 'pickRate2Rota',
            headerName: 'Pick Rate 2nd Rotation',
            width: 165,
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
            width: 160,
            renderCell: RenderDraftData
        },
        {
            field: 'banRate2Rota',
            headerName: 'Ban Rate 2nd Rotation',
            width: 165,
            renderCell: RenderDraftData
        },
        {
            field: 'blindPick',
            headerName: 'Blind Pick',
            width: 150,
            renderCell: RenderDraftData
        }
    ]

    

    const paginationModel = { page: 0, pageSize: 5 };

    return (
        <Paper sx={{ height: 370, width: 1700, justifySelf: "center"}}>
            <DataGrid
                rows={rows}
                columns={columns}
                initialState={{ pagination: { paginationModel } }}
                pageSizeOptions={[5, 10]}
                checkboxSelection
                sx={{ border: 0 }}
                
            />
        </Paper>
    )
}

export default DraftGrid