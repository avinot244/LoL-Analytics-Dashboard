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

/**
 * Returns a color based on the value (0-100).
 * 0 -> Red (#f44336)
 * 50 -> Orange (#ff9800)
 * 100 -> Green (#4caf50)
 */
const getColorForValue = (value) => {
    const clamp = (num, min, max) => Math.min(Math.max(num, min), max);
    value = clamp(value, 0, 100); // Ensure value is between 0 and 100.

    if (value <= 50) {
    // Transition from Red to Orange
    const t = value / 50; // Normalize to range [0, 1]
    return interpolateColor("#f44336", "#ff9800", t);
    } else {
    // Transition from Orange to Green
    const t = (value - 50) / 50; // Normalize to range [0, 1]
    return interpolateColor("#ff9800", "#4caf50", t);
    }
};