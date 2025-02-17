import { Box, Slider, Stack, Typography } from '@mui/material'
import { CustomMark } from './CustomMark'


function TimeFrameSelecter({gameDuration, value, setValue, gameEvents}) {
    
    // console.log(gameEvents)

    function valuetext(value) {
        return `${Math.floor(value/60)}min${value % 60}s`
    }

    const handleChange = (event, newValue) => {
        setValue(newValue)
    }

    let marks = [
    ]

    gameEvents.forEach(element => {
        marks.push({
            value: element.time,
            label: element.info
        })
    });

    

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
                    getAriaLabel={() => 'Temperature range'}
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
                    slots={{
                        markLabel: CustomMark
                    }}
                    objectivesTimeStamp={gameEvents}
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

export default TimeFrameSelecter