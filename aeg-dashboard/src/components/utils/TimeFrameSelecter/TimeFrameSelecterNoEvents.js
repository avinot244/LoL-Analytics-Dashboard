import { Box, Slider, Stack, Typography } from '@mui/material'


function TimeFrameSelecterNoEvent({gameDuration, value, setValue}) {    
    function valuetext(value) {
        return `${Math.floor(value/60)}min${value % 60}s`
    }

    const handleChange = (event, newValue) => {
        setValue(newValue)
    }

    let marks = [
        {
            "value": 90,
            "label": "1min30"
        },
        {
            "value": 840,
            "label": "14min"
        },
        {
            "value": 1500,
            "label": "25min"
        }

    ]

    

    return (
        <Box sx={{ width: "100%"}} alignSelf={"center"}>
            <Stack direction={"row"} spacing={5} alignSelf={"center"} alignItems={"center"}>
                <Typography
                    sx={{
                        width: "100px"
                    }}
                >
                    begTime : {valuetext(value[0])}
                </Typography>
                <Slider
                    getAriaLabel={() => 'Time Frame Selecter'}
                    value={value}
                    onChange={handleChange}
                    // valueLabelDisplay="on"
                    getAriaValueText={valuetext}
                    valueLabelFormat={valuetext}
                    max={gameDuration}
                    color='white'
                    marks={marks}
                    sx={{
                        '& .MuiSlider-markLabel': {
                            color: 'white',
                        },
                    }}
                />
                <Typography
                    x={{
                        width: "100px"
                    }}
                >
                    endTime : {valuetext(value[1])}
                </Typography>
            </Stack>
        </Box>
    )
}

export default TimeFrameSelecterNoEvent