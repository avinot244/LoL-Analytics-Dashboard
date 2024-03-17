import NavBarComp from "./NavbarComp";
import "../styles/ChampionOverview.css"

import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

import { amber,  brown,  grey} from '@mui/material/colors/'

import { useState } from "react";
import { ThemeProvider, createTheme } from "@mui/material";

function CustomTabPanel(props) {
    const { children, value, index, ...other } = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            className={`simple-tabpanel-${index}`}
            aria-labelledby={`simple-tab-${index}`}
            {...other}
        >
        {value === index && (
            <Box sx={{ p: 3 }}>
            <Typography>{children}</Typography>
            </Box>
        )}
        </div>
    );
}

const theme = createTheme({
    palette: {
        primary : {
            main: '#fff',
        }
    },
    action: {
        active: grey
    }
})


function ChampionOverview() {
    const [value, setValue] = useState(0)

    const handleChange = (event, newValue) => {
        setValue(newValue);
    }

    return(
        <div className="wrapper-overview">
            <NavBarComp />
            <h1> Champion overview </h1>
            <Box sx={{ borderBottom: 1, borderColor: 'black', width: 468}}> 
            <ThemeProvider theme={theme}>
                <Tabs 
                    value={value} 
                    onChange={handleChange}
                    textColor="primary"
                    indicatorColor="primary"
                >
                    <Tab 
                        label="Toplane"
                        sx={{
                            color:"gray"
                        }}
                    />
                    <Tab 
                        label="Jungle"
                        sx={{
                            color:"gray"
                        }}
                    />
                    <Tab 
                        label="Midlane"
                        sx={{
                            color:"gray"
                        }}
                    />
                    <Tab 
                        label="ADC"
                        sx={{
                            color:"gray"
                        }}
                    />
                    <Tab 
                        label="Support"
                        sx={{
                            color:"gray"
                        }}
                    />
                </Tabs>
            </ThemeProvider>
            </Box>
        
            
            <CustomTabPanel value={value} index={0}>
                Item Toplane
            </CustomTabPanel>
            <CustomTabPanel value={value} index={1}>
                Item Jungle
            </CustomTabPanel>
            <CustomTabPanel value={value} index={2}>
                Item Midlane
            </CustomTabPanel>
            <CustomTabPanel value={value} index={3}>
                Item ADC
            </CustomTabPanel>
            <CustomTabPanel value={value} index={4}>
                Item Support
            </CustomTabPanel>
        </div>
    )
}


export default ChampionOverview