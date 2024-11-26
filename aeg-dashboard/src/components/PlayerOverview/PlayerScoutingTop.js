import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import { Box, Autocomplete, TextField, Chip, createTheme, ThemeProvider, Stack, Button } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import ClearIcon from '@mui/icons-material/Clear'
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import RestartAltIcon from '@mui/icons-material/RestartAlt';

import AuthContext from '../context/AuthContext';
import GradientTypography from '../utils/GradientTypography';
import { API_URL } from '../../constants';
import Loading from '../utils/Loading';
import NormalDistribution from 'normal-distribution';

function RenderData(props) {
    const {_, value} = props
    return (
        <GradientTypography value={value} bold>{value}%</GradientTypography>
    )
}

const paginationModel = { page: 0, pageSize: 5 };


function TournamentFilter ({tournamentFilterList, selectedFilters, setSelectedFilters}) {
    const handleChange = (list) => {
        const newFilters = list
        setSelectedFilters(newFilters)
    }
    const theme = createTheme ({
        palette: {
            primary : {
                main: '#fff',
            },
            text : {
                disabled: '#fff'
            }
            
        },
        action: {
            active: '#fff'
        }
    })

    return (
        <>	
            <ThemeProvider theme={theme}>
                <Box sx={{ color: 'primary.main' , borderColor: 'white'}}>
                    <Autocomplete
                        multiple
                        clearIcon={<ClearIcon color="error"/>}
                        popupIcon={<ArrowDropDownIcon color="primary"/>}
                        className="searchComp"
                        options={tournamentFilterList}
                        renderInput={(params) => (
                            <TextField 
                                {...params} 
                                className='textField-searchComp'
                                label={"Tournament Filter"}
                                focused
                                sx={{ 
                                        input: { color: 'white'},
                                        borderColor: 'white'
                                    }}
                                
                            />
                        )}
                        renderTags={(value, getTagProps) => 
                            value.map((option, index) => (
                                <Chip
                                    color="primary"
                                    variant='outlined'
                                    label={option}
                                    {...getTagProps({index})}
                                />
                            ))
                        }
                        onChange={(_, value) => {handleChange(value)}}
                        sx={{color: 'primary.main', borderColor: 'primary.main', width: 550}}
                        fullWidth={true}
                    />
                </Box>
                
            </ThemeProvider>
        </>
	);
}

export default function PlayerScoutingTop(props){
    const {value, panelIndex} = props
    
    const [tournamentList, setTournamentList] = React.useState([])
    const [selectedFilters, setSelectedFilters] = React.useState([])
    const [loadingData, setLoadingData] = React.useState(true)
    const [flagDisplayData, setFlagDisplayData] = React.useState(false)

    const [rows, setRows] = React.useState([])
    const [columns, setColumns] = React.useState([])

    let {authTokens} = React.useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }
    
    const fetchData = async (tournamentList) => {
        setLoadingData(true)
        const modelResult = await fetch(API_URL + `behaviorModels/getModel/Top/`, {
            method: "GET",
            headers:header
        })
        modelResult.json().then(async model => {
            const jsonString = model.factorsName.replace(/'/g, '"')
            let factorsNameTemp = JSON.parse(jsonString)

            let newColumns = [
                {
                    field: 'playerName',
                    headerName: 'Player Name', 
                    width: 130
                }
            ]

            for (let i = 0 ; i < factorsNameTemp.length ; i ++) {
                newColumns.push({
                    field: factorsNameTemp[i].toLowerCase().replace(/[ /]/g, "_"),
                    headerName: factorsNameTemp[i],
                    renderCell: RenderData,
                    width: 150
                })
            }

            setColumns(newColumns)

            let data = {
                "wantedTournaments": tournamentList,
                "model_uuid": model.uuid
            }
    
            const dataResult = await fetch(API_URL + "behavior/Top/computeScouting/", {
                method: "PATCH",
                body: JSON.stringify(data),
                headers: header
            })

            dataResult.json().then(result => {
                const newData = result
                const normDist = new NormalDistribution(0, 1)
                let temp = []
                for (let i = 0; i < newData.summonnerName.length; i++) {
                    temp.push({
                        id: i,
                        playerName: newData.summonnerName[i],
                        aggression_w__jungle: ((1-normDist.cdf(newData.Factor_1[i]))*100).toFixed(2),
                        farming_safely: ((1-normDist.cdf(newData.Factor_2[i]))*100).toFixed(2),
                        tower_objective: ((1-normDist.cdf(newData.Factor_3[i]))*100).toFixed(2),
                        lane_player: ((1-normDist.cdf(newData.Factor_4[i]))*100).toFixed(2),
                        skirmish: ((1-normDist.cdf(newData.Factor_5[i]))*100).toFixed(2),
                        vision: ((1-normDist.cdf(newData.Factor_6[i]))*100).toFixed(2),
                    })
                }

                setRows(temp)
                setLoadingData(false)
            })
        })
    }

    const handleClick = () => {
        fetchData(selectedFilters)
        setFlagDisplayData(true)
    }

    React.useEffect(() => {
        const fetchTournamentList = async () => {
            const result = await fetch(API_URL + "dataAnalysis/tournament/getList", {
                method: "GET",
                headers: header
            })
            result.json().then(result => {
                const newTournamentList = result.sort();
                console.log(newTournamentList)
                setTournamentList(newTournamentList)
            })
        }
        
        fetchTournamentList();
    }, [])

    return (
        <div className="wrapper-player-scouting-Top">
            <div
                role='tabpanbel'
                hidden={value !== panelIndex}
                className={`simple-tabpanel-${panelIndex}`}
                aria-labelledby={`simple-tab-${panelIndex}`}
            >
                {
                    panelIndex === 0 && (
                        <>
                            <Stack spacing={2} direction="row" justifyContent="center" alignItems="center" sx={{pb: 2}}>
                                <TournamentFilter 
                                    tournamentFilterList={tournamentList}
                                    selectedFilters={selectedFilters}
                                    setSelectedFilters={setSelectedFilters}
                                />
                                <Button
                                    endIcon={<SearchIcon/>}
                                    variant='contained'
                                    onClick={() => handleClick()}
                                >
                                    Analyze
                                </Button>

                                <Button 
                                    variant="contained" 
                                    endIcon={<RestartAltIcon />}
                                    onClick={() => {
                                        setFlagDisplayData(false)
                                    }}    
                                >
                                    Reset
                                </Button>
                            </Stack>
                            {
                                flagDisplayData && (
                                    loadingData ? (
                                        <Loading/>
                                    ) : (
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
                                    )
                                )
                            }
                        </>
                    )
                }
            </div>
        </div>
    )
}