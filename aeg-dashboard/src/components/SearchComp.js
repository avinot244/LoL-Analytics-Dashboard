
import Select from 'react-select';
import "../styles/SelectComp.css"
import { useState } from 'react';
import { Autocomplete } from '@mui/material';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import { ThemeProvider, createTheme } from "@mui/material";
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';
import ClearIcon from '@mui/icons-material/Clear';

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




function SearchComp({selectedElement, setSelectedElement, elementList, label}) {
	const handleChange = (value) => {
		if (value != null) {
			console.log(value)
			setSelectedElement(value)
		}
	}
	return (	
		<>	
			
			<ThemeProvider theme={theme}>
				<Box sx={{ color: 'primary.main' , borderColor: 'white'}}>
					<Autocomplete
						clearIcon={<ClearIcon color="error"/>}
						popupIcon={<ArrowDropDownIcon color="primary"/>}
						id="searchComp"
						className="searchComp"
						options={elementList}
						renderInput={(params) => (
								<TextField 
									className='textField-searchComp'
									{...params} 
									label={label}
									sx={{ 
										input: { color: 'white'},
										borderColor: 'white'
									}}
									focused

								/>
							
							)}
						onChange={(_, value) => {handleChange(value)}}
						sx={{color: 'primary.main', borderColor: 'primary.main'}}
					/>
				</Box>
				
			</ThemeProvider>
		</>
	);
}

export default SearchComp;
