import { Box, Slider } from '@mui/material'
import { useState } from 'react'




function TimeFrameSelecter({gameDuration, value, setValue}) {
    

    function valuetext(value) {
        return `${Math.floor(value/60)}min${value % 60}s`
    }

    const handleChange = (event, newValue) => {
        setValue(newValue)
    }

    const marks = [
        {
            value: 60,
            label: `1min`
        },
        {
            value: 840,
            label: `14min`
        },
        {
            value: 1500,
            label: `25min`
        },
    ]

    return (
        <Box sx={{ width: 550, ml: 10 }}>
            <Slider
                getAriaLabel={() => 'Temperature range'}
                value={value}
                onChange={handleChange}
                valueLabelDisplay="on"
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
        </Box>
    )
}

export default TimeFrameSelecter