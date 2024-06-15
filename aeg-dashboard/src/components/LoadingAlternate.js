import { LinearProgress, Stack,ThemeProvider, createTheme } from "@mui/material";

const theme = createTheme({
    palette: {
        primary : {
            main: '#fff',
        }
    },
})

export default function LoadingAlternate () {
    return (
        <>
            <Stack spacing={2} direction="row" justifyContent="center" alignItems="center" sx={{pb: 2}}>
                <ThemeProvider theme={theme}>
                    <LinearProgress color="primary"/>
                </ThemeProvider>
            </Stack>
        </>
    )
}