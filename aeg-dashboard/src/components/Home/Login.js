import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';

import bgImage from "../../assets/login-bg.jpg"
import { useNavigate } from 'react-router-dom';
import { API_URL } from '../../constants';
import AuthContext from '../context/AuthContext';


// TODO remove, this demo shouldn't need to reset the theme.

const defaultTheme = createTheme({
    palette: {
        primary: {
            main: "#fff"
        }
    }
});



export default function SignInSide({loggedIn, setLoggedIn}) {
    const [userName, setUserName] = React.useState("")
    const [password, setPassword] = React.useState("")
    const [error, setError] = React.useState("")
    const [authTokens, setAuthTokens] = React.useState(null)

    let {login} = React.useContext(AuthContext)

    const navigate = useNavigate()

    function getSession() {
        fetch(API_URL + "authentication/session/", {
            credentials: "same-origin"
        })
        .then((res) => res.json())
        .then((data)=>{
            console.log(data)
            if (data.isauthenticated) {
                setLoggedIn(true)
            }else{
                setLoggedIn(false)
            }
        })
        .catch((err) => {
            console.log(err)
        })
    }

    function whoami() {
        fetch(API_URL + "authentication/whoami/", {
            headers: {
                "Content-type": "application/json"
            },
            credentials: "same-origin"
        })
        .then((res) => res.json())
        .then((data) => {
            console.log("you're logged in as" + data.username)
        })
        .catch((err) => {
            console.log(err)
        })
    }

    function handlePasswordChange(event) {
        setPassword(event.target.value)
    }

    function handleUserNameChange(event) {
        setUserName(event.target.value)
    }

    function isResponseOk(response) {
        if (response.status >= 200 && response.status <= 299) {
            return response.json();
        }else{
            throw Error(response.statusText)
        }
    }

    const handleSubmit = async (event) => {
        event.preventDefault();
        let bool = await login(userName, password)
        console.log(bool)

        if (bool) {
            console.log("OOOK")
            navigate("/Home")
        }else{
            setError("Wrong username or password")
        }
    };

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
                        <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                            <LockOutlinedIcon />
                        </Avatar>
                        <Typography component="h1" variant="h5" color={"white"}>
                            Sign in
                        </Typography>
                        <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 1 }}>
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                id="username"
                                label="Username"
                                name="username"
                                autoComplete="username"
                                focused
                                sx={{ 
                                    input: { color: 'white'},
                                }}
                                onChange={handleUserNameChange}
                            />
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                name="password"
                                label="Password"
                                type="password"
                                id="password"
                                autoComplete="current-password"
                                focused
                                sx={{ 
                                    input: { color: 'white'},
                                }}
                                onChange={handlePasswordChange}
                            />
                            {error !== "" && <Typography component="div" variant='p' color={"red"}>{error}</Typography>}
                            <Button
                                type="submit"
                                fullWidth
                                variant="contained"
                                sx={{ mt: 3, mb: 2 }}
                            >
                                Sign In
                            </Button>
                            <Grid container>
                                <Grid item xs>
                                    <Link href="#" variant="body2">
                                        Forgot password?
                                    </Link>
                                </Grid>
                                <Grid item>
                                    <Link href="#" variant="body2">
                                        {"Don't have an account? Sign Up"}
                                    </Link>
                                </Grid>
                            </Grid>
                        </Box>
                    </Box>
                </Grid>
            </Grid>
        </ThemeProvider>
    );
}