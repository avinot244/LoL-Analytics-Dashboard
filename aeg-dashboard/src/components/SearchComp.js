
import Select from 'react-select';
import "../styles/SelectComp.css"
import { useState } from 'react';
import { Autocomplete } from '@mui/material';
import { TextField } from '@mui/material';
import Box from '@mui/material/Box';

import { amber,  brown,  grey} from '@mui/material/colors/'
import { ThemeProvider, createTheme } from "@mui/material";


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

function SearchComp({selectedElement, setSelectedElement, elementList}) {
	return (	
		<>	
			<ThemeProvider theme={theme}>
				<Box sx={{ color: 'primary.main' , borderColor: 'white'}}>
					<Autocomplete
						disablePortal
						id="searchComp"
						className="searchComp"
						options={elementList}
						renderInput={(params) => {
							return (
								<TextField 
									sx={{color:'primary.main'}} 
									className='textField-searchComp'
									{...params} 
									label="Player"
								/>
							)
							
						}}
						onChange={(element) => setSelectedElement(element.value)}
						sx={{color: 'primary.main', borderColor: 'primary.main'}}
					/>
				</Box>
				
			</ThemeProvider>
		</>
	);
}

export default SearchComp;
