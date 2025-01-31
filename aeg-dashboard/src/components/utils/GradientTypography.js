import interpolateColor from "./utils_func";
import { Typography } from "@mui/material";

const getColorForValue = (value) => {
    const clamp = (num, min, max) => Math.min(Math.max(num, min), max);
    value = clamp(value, 0, 100); // Ensure value is between 0 and 100.

    if (value <= 50) {
    // Transition from Green to Orange
    const t = value / 50; // Normalize to range [0, 1]
    return interpolateColor("#4caf50", "#ff9800", t);
    } else {
    // Transition from Orange to Red
    const t = (value - 50) / 50; // Normalize to range [0, 1]
    return interpolateColor("#ff9800", "#f44336", t);
    }
};

export default function GradientTypography ({value, children, bold}) {
    const color = getColorForValue(value);

    return (
        <>
            {
                !bold ? (  
                    <Typography style={{color}}>
                        {children}
                    </Typography>
                ) : (
                    <Typography style={{color, fontWeight: 'bold'}}>
                        {children}
                    </Typography>
                )
            }
        </>
    )
}