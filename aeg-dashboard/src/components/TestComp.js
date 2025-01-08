import NavBarComp from "./utils/NavbarComp"
import "../styles/TestComp.css"

import { Typography } from "@mui/material"

import Plot from "react-plotly.js"


function TestComp() {
    // Example data
    const x = Array.from({ length: 1000 }, () => Math.random() * 10);
    const y = Array.from({ length: 1000 }, () => Math.random() * 10);

    return (
        <div className="wrapper-Test">
            <NavBarComp/>
            <Typography id="title-Test" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold", mb: 10}}>
                Test page
            </Typography>

            <div className="wrapper-plot">
                <Plot
                    data={[
                        {
                            x,
                            y,
                            type: 'histogram2d',
                            colorscale: 'Blues', // Shading color scheme
                        },
                    ]}
                    layout={{
                        title: '2D Density Plot with Shading',
                        xaxis: { title: 'X Axis' },
                        yaxis: { title: 'Y Axis' },
                    }}
                    config={{ responsive: true }}
                    style={{ width: '100%', height: '100%' }}
                />
            </div>
            
        </div>
    )
}

export default TestComp