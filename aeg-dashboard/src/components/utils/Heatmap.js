import React, { useEffect, useRef } from 'react';
import h337 from 'heatmap.js';
import { Button, Stack } from '@mui/material';

function gaussianKernel(x, sigma = 1.0) {
    // x is the difference between data points (or distance)
    return Math.exp(-Math.pow(x, 2) / (2 * Math.pow(sigma, 2)));
}

/**
 * Calculate Kernel Density Estimation (KDE) for a set of coordinates.
 * @param {Array} points - An array of coordinates [{x, y}].
 * @param {number} bandwidth - The bandwidth (standard deviation of the kernel).
 * @returns {Array} - An array of points with density values.
 */
function calculateKDE(points, bandwidth) {
    const densityPoints = [];

    // For KDE, we create a smooth grid of estimated densities
    points.forEach((point) => {
        let totalDensity = 0;

        // Calculate the density at each point in the grid
        points.forEach((neighbor) => {
            if (point !== neighbor) {
                const distance = Math.sqrt(Math.pow(point.x - neighbor.x, 2) + Math.pow(point.y - neighbor.y, 2));
                totalDensity += gaussianKernel(distance, bandwidth);  // Gaussian kernel density
            }
        });
        // Add the density information to the list
        densityPoints.push({
            ...point,
            value: totalDensity,
        });
    });

    return densityPoints;
}


const Heatmap = ({ data, bandwidth, resolution, backgroundImage }) => {
    const heatmapContainerRef = useRef(null);
    const heatmapInstanceRef = useRef(null);

    // Initialize the heatmap when the component is mounted
    useEffect(() => {
        // Calculate density using KDE
        const densityPoints = calculateKDE(data, bandwidth);
        // Initialize the heatmap.js
        heatmapInstanceRef.current = h337.create({
            container: heatmapContainerRef.current,
            radius: 10, // Adjust for smoother points
            maxOpacity: 0.6,
            minOpacity: 0,
            blur: 0.75,
            gradient: {
                0.4: 'blue',
                0.6: 'green',
                0.8: 'yellow',
                1.0: 'red',
            },
        });

        // Set the KDE data into the heatmap
        heatmapInstanceRef.current.setData({
            max: Math.max(...densityPoints.map((p) => p.value)),  // Set max density
            min: Math.min(...densityPoints.map((p) => p.value)),
            data: densityPoints,  // Points with density values
        });
        return () => {
            // Clean up the heatmap instance on component unmount
            heatmapInstanceRef.current = null;
        };
    }, [data, bandwidth, resolution]);

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
};

export default Heatmap;
