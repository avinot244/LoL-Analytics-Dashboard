import * as React from 'react';
import { Autocomplete, Chip, ThemeProvider, createTheme } from '@mui/material';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import ClearIcon from '@mui/icons-material/Clear'

import '../../styles/Monitoring.css'


function MultipleSearchComp({tournamentFilterList, selectedFilters, setSelectedFilters}) {
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
                        sx={{color: 'primary.main', borderColor: 'primary.main', width: 200}}
                        fullWidth={true}
                    />
                </Box>
                
            </ThemeProvider>
        </>
	);
}

export default MultipleSearchComp