import { CircularProgress, Stack } from "@mui/material"
import { ThemeProvider, createTheme } from "@mui/material";

const theme = createTheme({
    palette: {
        primary : {
            main: '#fff',
        }
    },
})

export default function Loading () {
    return (
        <>
            <Stack spacing={2} direction="row" justifyContent="center" alignItems="center" sx={{pb: 2}}>
                <ThemeProvider theme={theme}>
                    <CircularProgress color="primary"/>
                </ThemeProvider>
            </Stack>
        </>
        
    )
}