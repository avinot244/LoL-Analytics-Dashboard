import "../../styles/ScatterPlot.css"

import React, { useEffect, useRef } from 'react';
import h337 from 'heatmap.js';

import { Button, Stack } from '@mui/material';

const ScatterPlot = ({data, backgroundImage, side}) => {

    const heatmapContainerRef = useRef(null);
    const heatmapInstanceRef = useRef(null);
    
    let color = ""
    if (side === "Blue") {
        color = "cyan"
    }else{
        color = "red"
    }

    // Initialize the heatmap when the component is mounted
    useEffect(() => {
        // Calculate density using KDE
        // Initialize the heatmap.js
        heatmapInstanceRef.current = h337.create({
            container: heatmapContainerRef.current,
            radius: 10, // Adjust for smoother points
            maxOpacity: 1,
            minOpacity: 0,
            blur: 0.75,
            gradient: {
                1.0: color,
            },
        });

        // Set the KDE data into the heatmap
        heatmapInstanceRef.current.setData({
            max: Math.max(data),  // Set max density
            min: Math.min(data),
            data: data,  // Points with density values
        });
        return () => {
            // Clean up the heatmap instance on component unmount
            heatmapInstanceRef.current = null;
        };
    }, [data]);
    
    const clearData = () => {
        if (heatmapInstanceRef.current) {
            heatmapInstanceRef.current.setData({
            max: 0,
            data: [], // Pass an empty dataset
            });
        }
    };

    return (
        <Stack
            direction="column"
            alignItems="center"
            justifyContent="center"
            spacing={2}
        >
            <div ref={heatmapContainerRef} style={{ 
                position: 'relative', // Relative positioning
                height: '500px', // 10/295 ratio original size : 14750px
                width: '500px',
                backgroundImage: `url(${backgroundImage})`, // Local image as background
                backgroundSize: 'cover', // Adjust image size
                backgroundPosition: 'center', // Center the image
                backgroundRepeat: 'no-repeat', // Avoid repeating the image
                margin: '0px auto'
            }} />
            <Button
                variant='contained'
                onClick={() => clearData()}
            >
                Clear Data
            </Button>
        </Stack>
    );
}


export default ScatterPlot