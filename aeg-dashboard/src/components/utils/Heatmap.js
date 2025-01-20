import React, { useEffect, useRef, useImperativeHandle, forwardRef } from 'react';
import h337 from 'heatmap.js';
import { Stack } from '@mui/material';

function gaussianKernel(x, sigma = 1.0) {
    return Math.exp(-Math.pow(x, 2) / (2 * Math.pow(sigma, 2)));
}

function calculateKDE(points, bandwidth) {
    const densityPoints = [];
    points.forEach((point) => {
        let totalDensity = 0;
        points.forEach((neighbor) => {
            if (point !== neighbor) {
                const distance = Math.sqrt(Math.pow(point.x - neighbor.x, 2) + Math.pow(point.y - neighbor.y, 2));
                totalDensity += gaussianKernel(distance, bandwidth);
            }
        });
        densityPoints.push({
            ...point,
            value: totalDensity,
        });
    });
    return densityPoints;
}

const Heatmap = forwardRef(({ data, bandwidth, resolution, backgroundImage, size }, ref) => {
    const heatmapContainerRef = useRef(null);
    const heatmapInstanceRef = useRef(null);

    useEffect(() => {
        const densityPoints = calculateKDE(data, bandwidth);
        heatmapInstanceRef.current = h337.create({
            container: heatmapContainerRef.current,
            radius: 10,
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

        heatmapInstanceRef.current.setData({
            max: Math.max(...densityPoints.map((p) => p.value)),
            min: Math.min(...densityPoints.map((p) => p.value)),
            data: densityPoints,
        });

        return () => {
            heatmapInstanceRef.current = null;
        };
    }, [data, bandwidth, resolution]);

    const clearData = () => {
        if (heatmapInstanceRef.current) {
            heatmapInstanceRef.current.setData({
                max: 0,
                data: [],
            });
        }
    };

    // Expose the `clearData` function to the parent through the ref
    useImperativeHandle(ref, () => ({
        clearData,
    }));

    return (
        <Stack
            direction="column"
            alignItems="center"
            justifyContent="center"
            spacing={2}
        >
            <div
                ref={heatmapContainerRef}
                style={{
                    position: 'relative',
                    height: `${size}px`,
                    width: `${size}px`,
                    backgroundImage: `url(${backgroundImage})`,
                    backgroundSize: 'cover',
                    backgroundPosition: 'center',
                    backgroundRepeat: 'no-repeat',
                    margin: '0px auto',
                }}
            />
        </Stack>
    );
});

export default Heatmap;
