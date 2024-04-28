
import "../styles/SelectComp.css"
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




function SearchComp({setSelectedElement, elementList, label, width}) {
	const handleChange = (value) => {
		if (value != null) {
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
						sx={{color: 'primary.main', borderColor: 'primary.main', width: width}}
					/>
				</Box>
				
			</ThemeProvider>
		</>
	);
}

export default SearchComp;
