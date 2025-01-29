import { Select, InputLabel, FormControl, Box, MenuItem, createTheme, ThemeProvider } from '@mui/material';

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

function SelectComp({elementList, value, setValue, label}) {
	return (
		<ThemeProvider theme={theme}>
			<Box sx={{ minWidth: 120, color: 'primary.main' , borderColor: 'white'}}>
				<FormControl fullWidth>
					<InputLabel id="demo-simple-select-label">{label}</InputLabel>
					<Select
						labelId="demo-simple-select-label"
						id="demo-simple-select"
						value={value}
						label={label}
						variant='outlined'
						onChange={(e) => setValue(e.target.value)}
						sx={{
							color: 'primary.main', 
							borderColor: 'primary.main',
							".Mui-focused": 'primary.main',
							".MuiSelect-icon": {
								color: 'primary.main'
							},
						}}
					>
						{elementList.map((element) => (
							<MenuItem
								sx={{
									
								}}
							>
								{element}
							</MenuItem>
						))}
					</Select>
				</FormControl>
			</Box>
		</ThemeProvider>
	)
}

export default SelectComp;