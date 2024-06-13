import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import ReportIcon from '@mui/icons-material/Report';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Nav from 'react-bootstrap/Nav';


import { Link } from 'react-router-dom';

import bgImage from "../../assets/redirect-bg.jpg"

const defaultTheme = createTheme({
    palette: {
        primary: {
            main: "#fff"
        },
        error: {
            main: "#f44336"
        }
    }
});

export default function RedirectPage() {
    return (
        <ThemeProvider theme={defaultTheme}>
            <Grid container component="main" sx={{ height: '100vh' }}>
                <CssBaseline />
                <Grid
                    item
                    xs={false}
                    sm={4}
                    md={7}
                    sx={{
                        backgroundImage: `url(${bgImage})`,
                        backgroundRepeat: 'no-repeat',
                        backgroundColor: (t) =>
                            t.palette.mode === 'light' ? t.palette.grey[50] : t.palette.grey[900],
                        backgroundSize: 'cover',
                        backgroundPosition: 'center',
                    }}
                />
                <Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square sx={{backgroundColor: "#282c34"}}>
                    <Box
                        sx={{
                            my: 8,
                            mx: 4,
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                        }}
                    >
                        <Avatar sx={{ m: 1, bgcolor: '#f44336', width: 100, height: 100}}>
                            <ReportIcon sx={{width: 100, height: 100}} />
                        </Avatar>
                        <Typography component="h1" variant="h5" color={"white"}>
                            ERROR
                        </Typography>
                        <Box component="form" noValidate sx={{ mt: 1 }}>
                            <Typography component="h2" variant="subtitle1" color={"white"}>
                                You are not allowed to access this website without authentication
                            </Typography>
                            <Typography component="h2" variant="subtitle1" color={"white"}>
                                Please go to the log in page bellow to access the tool
                            </Typography>
                            <Nav.Link as={Link} to="/">
                                <Button
                                    fullWidth
                                    variant="contained"
                                    sx={{ mt: 3, mb: 2 }}
                                >
                                    Go to Log In
                                </Button>
                            </Nav.Link>
                        </Box>
                    </Box>
                </Grid>
            </Grid>
        </ThemeProvider>
    )
}