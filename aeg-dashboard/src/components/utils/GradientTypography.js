import getColorForValue from "./utils_func";
import { Typography } from "@mui/material";

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