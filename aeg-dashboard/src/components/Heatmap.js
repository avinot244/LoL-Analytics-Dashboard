import React, { useEffect, useRef, useState } from 'react';
import h337 from 'heatmap.js';

function gaussianKernel(x, sigma = 1.0) {
    // x is the difference between data points (or distance)
    return Math.exp(-Math.pow(x, 2) / (2 * Math.pow(sigma, 2)));
}

/**
 * Calculate Kernel Density Estimation (KDE) for a set of coordinates.
 * @param {Array} points - An array of coordinates [{x, y}].
 * @param {number} bandwidth - The bandwidth (standard deviation of the kernel).
 * @param {number} resolution - The number of points to estimate density.
 * @returns {Array} - An array of points with density values.
 */
function calculateKDE(points, bandwidth, resolution) {
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

    // Initialize the heatmap when the component is mounted
    useEffect(() => {
        // Calculate density using KDE
        const densityPoints = calculateKDE(data, bandwidth, resolution);
        // Initialize the heatmap.js
        const heatmap = h337.create({
            container: heatmapContainerRef.current,
            radius: 10, // Adjust for smoother points
            maxOpacity: 0.5,
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
        heatmap.setData({
            max: Math.max(...densityPoints.map((p) => p.value)),  // Set max density
            min: Math.min(...densityPoints.map((p) => p.value)),
            data: densityPoints,  // Points with density values
        });
    }, [data, bandwidth, resolution]);

    
    return <div ref={heatmapContainerRef} style={{ 
        position: 'relative', // Relative positioning
        height: '500px', // 10/295 ratio original size : 14750px
        width: '500px',
        backgroundImage: `url(${backgroundImage})`, // Local image as background
        backgroundSize: 'cover', // Adjust image size
        backgroundPosition: 'center', // Center the image
        backgroundRepeat: 'no-repeat', // Avoid repeating the image
        margin: '0px auto'
    }} />;
};

export default Heatmap;
