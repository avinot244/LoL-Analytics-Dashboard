import * as React from 'react';
import Button from '@mui/material/Button';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import DownloadIcon from '@mui/icons-material/Download';
import { Autocomplete, Chip } from '@mui/material';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import { ThemeProvider, createTheme } from "@mui/material";
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import ClearIcon from '@mui/icons-material/Clear'
import SearchIcon from '@mui/icons-material/Search';
import Stack from '@mui/material/Stack';


import '../../styles/Monitoring.css'

import NavBarComp from '../NavbarComp.js';
import { API_URL } from '../../constants/index.js';
;

function TournamentSelecter({onRemove, onSelectChange, tournamentList}) {
    const [selectedTournament, setSelectedTournament] = React.useState('')
    const handleSelectChange = (value) => {
        const newValue = value;
        setSelectedTournament(newValue)
        onSelectChange(newValue)
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
            <Stack spacing={2} direction="row" justifyContent="center" alignItems="center" sx={{pb: 2}}>
                <>	
                    <ThemeProvider theme={theme}>
                        <Box sx={{ color: 'primary.main' , borderColor: 'white'}}>
                            <Autocomplete
                                clearIcon={<ClearIcon color="error"/>}
                                popupIcon={<ArrowDropDownIcon color="primary"/>}
                                className="searchComp"
                                options={tournamentList}
                                renderInput={(params) => (
                                    <TextField 
                                        className='textField-searchComp'
                                        {...params} 
                                        label={"Tournament"}
                                        sx={{ 
                                            input: { color: 'white'},
                                            borderColor: 'white'
                                        }}
                                        focused
                                        fullWidth={true}

                                    />
                                    
                                )}
                                onChange={(_, value) => {handleSelectChange(value)}}
                                sx={{color: 'primary.main', borderColor: 'primary.main', width: 525}}
                                fullWidth={true}
                            />
                        </Box> 
                    </ThemeProvider>
                </>
                <Button
                    onClick={onRemove}
                    color='error'
                    variant='contained'
                    startIcon={<DeleteIcon/>}
                >
                    Remove
                </Button>
        </Stack>
    )
}

const fetchData = async (tournamentList) => {
    try {
        const strTournamentList = tournamentList.join(',')
        const response = await fetch(API_URL + `dataAnalysis/updateDatabase/${strTournamentList}/`,{
            method: "PATCH"
        });
        const data = await response.json();
        console.log(data)
    } catch (error) {
        console.error('Error fetch data:', error)
    }
}

function TextAdder({selectedTournaments, setSelectedTournaments, tournamentList}) {
    // State to store the paragraphs
    const [paragraphs, setParagraphs] = React.useState([]);
    

    // Function to add a paragraph
    const addParagraph = () => {
        const newParagraphs = [...paragraphs, `Paragraph ${paragraphs.length + 1}`];
        setParagraphs(newParagraphs);
        setSelectedTournaments([...selectedTournaments, ''])
    };

    // Function to remove a paragraph by index
    const removeParagraph = (index) => {
        const newParagraphs = [...paragraphs];
        newParagraphs.splice(index, 1);
        setParagraphs(newParagraphs);

        const newSelectTournaments = [...selectedTournaments];
        newSelectTournaments.splice(index, 1);
        setSelectedTournaments(newSelectTournaments)
    };

    const handleSelectChange = (value, index) => {
        const newSelectedTournaments = [...selectedTournaments]
        newSelectedTournaments[index] = value;
        setSelectedTournaments(newSelectedTournaments)
    }

    const handleDownload = () => {
        let flag = true
        if (selectedTournaments.length === 0) {
            flag = false
        }
        for (let i = 0 ; i < selectedTournaments.length ; i++) {
            if (selectedTournaments[i] === ""){
                flag = false
            }
        }

        if (flag) {
            fetchData(selectedTournaments)
        }else{
            alert("Please select a tournament in each fields")
        }
    }


    return (
        <div className='tournamentSelect-wrapper'>
            <div>
                {paragraphs.map((paragraph, index) => (
                    <TournamentSelecter
                        key={index}
                        text={paragraph}
                        onRemove={() => removeParagraph(index)}
                        onSelectChange={(value) => handleSelectChange(value, index)}
                        tournamentList={tournamentList}
                    />
                ))}
            </div>

            <div className='wrapper-button-tournamentSelect'>
                <Button
                    onClick={addParagraph}
                    variant='contained'
                    startIcon={<AddIcon/>}
                    sx = {{
                        mr: 2
                    }}
                >
                    Add Tournament
                </Button>

                <Button
                    variant='contained'
                    endIcon={<DownloadIcon/>}
                    color="success"
                    onClick={() => handleDownload()}
                >
                    Download
                </Button>
            </div>
        </div>
    );
}


function TournamentFilter({tournamentFilterList, selectedFilters, setSelectedFilters}) {
    const handleChange = (list) => {
        const newFilters = list
        setSelectedFilters(newFilters)
        console.log(selectedFilters)
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
                        sx={{color: 'primary.main', borderColor: 'primary.main', width: 200}}
                        fullWidth={true}
                    />
                </Box>
                
            </ThemeProvider>
        </>
	);
}



export default function Downloader() {
    const [tournamentList, setTournamentList] = React.useState([]);
    const [selectedTournaments, setSelectedTournaments] = React.useState([]);
    const [tournamentListShortended, setTournamentListShortened] = React.useState([])
    const [selectedFilters, setSelectedFilters] = React.useState([])


    const [flagDisplay, setFlagDisplay] = React.useState(false)

    const fetchTournamentList = async () => {
        const today = new Date()
        const year = today.getFullYear();
        const result = await fetch(API_URL + `dataAnalysis/getListDownlodableTournament/${year}/`, {
            method: "POST",
            body: JSON.stringify(selectedFilters)
        })
        result.json().then(result => {
            console.log(result)
            let newTournamentList = Object.keys(result)
            console.log(newTournamentList)
            newTournamentList = newTournamentList.sort()
            setTournamentList(newTournamentList)
        })
    }

    const fetchTournamentFilterList = async () => {
        const result = await fetch(API_URL + `dataAnalysis/getTournamentListShortened/`, {
            method: "GET"
        })
        result.json().then(result => {
            let newTournamentListShortended = result.sort()
            setTournamentListShortened(newTournamentListShortended)
        })
    }

    React.useEffect(() => {
        fetchTournamentFilterList()
    }, [])



    return (
        <div className='wrapper-downloader'>
            <NavBarComp/>
            <h1>Download Games</h1>
            

            <h2>Select the tournament filter</h2>
            <Stack spacing={2} direction="row" justifyContent="center" alignItems="center" sx={{pb: 2}}>
                <TournamentFilter
                    tournamentFilterList={tournamentListShortended}
                    selectedFilters={selectedFilters}
                    setSelectedFilters={setSelectedFilters}
                />
                <Button
                    endIcon={<SearchIcon/>}
                    variant='contained'
                    onClick={() => {fetchTournamentList(); setFlagDisplay(true)}}
                    
                >
                    Get Tournaments
                </Button>

            </Stack>
            

            {
                flagDisplay &&
                <TextAdder
                    tournamentList={tournamentList}
                    selectedTournaments={selectedTournaments}
                    setSelectedTournaments={setSelectedTournaments}
                />
            }
            
        
        
        </div>
    );
}