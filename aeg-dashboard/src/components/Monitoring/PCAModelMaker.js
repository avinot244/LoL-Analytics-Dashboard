import NavBarComp from "../utils/NavbarComp";
import "../../styles/PCAModelMaker.css"

import * as React from 'react';
import Button from '@mui/material/Button';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import { ThemeProvider, createTheme, Typography, Autocomplete } from "@mui/material";
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import ClearIcon from '@mui/icons-material/Clear'
import DeveloperBoardIcon from '@mui/icons-material/DeveloperBoard';
import Stack from '@mui/material/Stack';

import { API_URL, roleList } from '../../constants/index.js';
import AuthContext from "../context/AuthContext.js";
import SearchComp from "../utils/SearchComp.js";

function TournamentSelecter({onRemove, onSelectChange, tournamentList, tournamentDict, flagOverflow, setFlagOverflow}) {
    const [selectedTournament, setSelectedTournament] = React.useState({"League of Legends Scrims": 0})
    const [amount, setAmount] = React.useState(0)
    
    const handleAmountChange = (amount) => {
        let temp = Object.keys(selectedTournament)[0]

        let limit = Object.values(tournamentDict[tournamentList.indexOf(temp)])[0]
        let newValue = {}

        if (amount <= limit) {
            newValue = {[Object.keys(selectedTournament)[Object.keys(selectedTournament).length-1]]: parseInt(amount, 10)}
            setFlagOverflow(false)
        }else {
            newValue = {[Object.keys(selectedTournament)[Object.keys(selectedTournament).length-1]]: parseInt(limit, 10)}
            setFlagOverflow(true)
        }

            
        setSelectedTournament(newValue)
        onSelectChange(newValue)
    }

    const handleSelectChange = (value) => {
        const newValue = {[value]:amount};
        setSelectedTournament(newValue)
        onSelectChange(newValue)
    }

    const theme = createTheme ({
        palette: {
            primary : {
                main: '#fff',
                error: '#e57373'
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
                            renderInput={(params) => {
                                if (flagOverflow) {
                                    return (
                                        <TextField 
                                            className='textField-searchComp'
                                            {...params} 
                                            label={"Tournament"}
                                            sx={{ 
                                                input: { color: 'red'},
                                            }}
                                            focused
                                            fullWidth={true}

                                        
                                        />
                                    )
                                }else {
                                    return (
                                            
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
                                        
                                    )
                                }
                            }}
                                
                                
                            onChange={(_, value) => {handleSelectChange(value)}}
                            sx={{color: 'primary.main', borderColor: 'primary.main', width: 525}}
                            fullWidth={true}
                        />
                    </Box> 
                </ThemeProvider>
            </>

            <ThemeProvider theme={theme}>
                <TextField
                    id="outlined-number"
                    label="Games"
                    type="number"
                    InputLabelProps={{
                        shrink: true,
                    }}
                    sx={{ 
                        input: { color: 'white'},
                        borderColor: 'white'
                    }}
                    focused
                    onChange={(e) => {
                        handleAmountChange(e.target.value)
                    }}
                />
            </ThemeProvider>
            <p>max : {Object.values(tournamentDict[tournamentList.indexOf(Object.keys(selectedTournament)[0])])[0]}</p>
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

const fetchData = async (tournamentList, role, authTokens) => {
    let res = {}
    console.log(role)
    let header = {
        Authorization: authTokens.access
    }
    tournamentList.map((object) => res[Object.keys(object)] = Object.values(object)[0])
    let response = await fetch(API_URL + `behaviorModels/${role}/computeModel`, {
        method: "POST",
        body: JSON.stringify(res),
        headers:header
    })
    response.json().then((newModel) => {
        console.log(newModel)
    })
}

function TextAdder({selectedTournaments, setSelectedTournaments, tournamentList, tournamentDict, activeRole, authTokens}) {
    // State to store the paragraphs
    const [paragraphs, setParagraphs] = React.useState([]);
    const [flagOverflow, setFlagOverflow] = React.useState(false)
    

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

    const handleCompute = () => {
        let flag = true
        if (selectedTournaments.length === 0) {
            flag = false
        }
        for (let i = 0 ; i < selectedTournaments.length ; i++) {
            if (selectedTournaments[i] === ""){
                flag = false
            }
        }

        if (flagOverflow) {
            alert("Too much game selected for given tournament")
        }else{
            if (flag) {
                fetchData(selectedTournaments, activeRole, authTokens)            
            }else{
                alert("Please select a tournament in each fields")
            }
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
                        tournamentDict={tournamentDict}
                        flagOverflow={flagOverflow}
                        setFlagOverflow={setFlagOverflow}
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
                    endIcon={<DeveloperBoardIcon/>}
                    color="success"
                    onClick={() => handleCompute()}
                >
                    Compute model
                </Button>
            </div>
        </div>
    );
}


export default function PCAModelMaker() {
    const [tournamentList, setTournamentList] = React.useState([]);
    const [tournamentDict, setTournamentDict] = React.useState([])
    const [selectedTournaments, setSelectedTournaments] = React.useState([]);
    const [activeRole, setActiveRole] = React.useState('')

    let {authTokens} = React.useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }

    const fetchTournamentList = async () => {
        const result = await fetch(API_URL + `dataAnalysis/tournament/getDict`, {
            method: "GET",
            headers:header
        })
        result.json().then(result => {
            let newTournamentList = []
            result.map((tournamentObject) => newTournamentList.push(Object.keys(tournamentObject)[0]))
            newTournamentList = newTournamentList
            
            setTournamentList(newTournamentList)

            let newTournamentDict = result
            setTournamentDict(newTournamentDict)
        })
    }



    React.useEffect(()=>{
        fetchTournamentList()
    }, [])

    return (
        <div className="pca-model-maker-wrapper">
            <NavBarComp/>

            <Typography id="PCAdocumentation-title" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold", mb: 10}}>
                Create Behavior Analysis Models
            </Typography>

            <div className="PCAMaker-control-panel">
                <div className="PCAMaker-roleSelected-wrapper">
                    <h3>Select a role</h3>
                    <div className="PCAMaker-roleSelecter">
                        <SearchComp
                            elementList={roleList}
                            defaultValue={"-- Role --"}
                            setSelectedElement={setActiveRole}
                            label={"Role"}
                            width={150}
                        />

                    </div>
                </div>
                    
                <div className="PCAMaker-tournament-selecter">
                    <h3>Select a list of tournaments</h3>
                    <TextAdder
                        tournamentList={tournamentList}
                        selectedTournaments={selectedTournaments}
                        setSelectedTournaments={setSelectedTournaments}
                        tournamentDict={tournamentDict}
                        activeRole={activeRole}
                        authTokens={authTokens}
                    />
                </div>
                
            </div>
        </div>
    )
}