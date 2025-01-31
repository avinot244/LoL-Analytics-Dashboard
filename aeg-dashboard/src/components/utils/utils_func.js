const interpolateColor = (color1, color2, t) => {
    const hexToRgb = (hex) => {
        const match = hex.match(/^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i);
        return match
            ? [
                parseInt(match[1], 16),
                parseInt(match[2], 16),
                parseInt(match[3], 16),
            ]
            : [0, 0, 0];
    };
    
    const rgb1 = hexToRgb(color1);
    const rgb2 = hexToRgb(color2);

    const r = Math.round(rgb1[0] + t * (rgb2[0] - rgb1[0]));
    const g = Math.round(rgb1[1] + t * (rgb2[1] - rgb1[1]));
    const b = Math.round(rgb1[2] + t * (rgb2[2] - rgb1[2]));

    return `rgb(${r}, ${g}, ${b})`;
};

export default interpolateColor