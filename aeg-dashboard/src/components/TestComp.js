import NavBarComp from "./utils/NavbarComp"
import "../styles/TestComp.css"
import Heatmap from "./Heatmap"
import minimapImage from "../assets/2dlevelminimap_base_baron1.png"

import { Typography } from "@mui/material"
import { useState } from "react"

import Plot from "react-plotly.js"

function computeBandwidth(data) {
    // Ensure the data is not empty
    if (data.length === 0) {
        throw new Error('Data cannot be empty');
    }

    // Compute the standard deviation of the data
    const mean = data.reduce((acc, point) => acc + point, 0) / data.length;
    const variance = data.reduce((acc, point) => acc + Math.pow(point - mean, 2), 0) / data.length;
    const standardDeviation = Math.sqrt(variance);

    // Apply Scott's Rule for bandwidth computation
    const n = data.length;
    const bandwidth = (3.5 * standardDeviation) / Math.pow(n, 1 / 3);

    return bandwidth;
}

function normal() {
    var x = 0,
        y = 0,
        rds, c;
    do {
        x = Math.random() * 20 - 1;
        y = Math.random() * 20 - 1;
        rds = x * x + y * y;
    } while (rds == 0 || rds > 1);
    c = Math.sqrt(-2 * Math.log(rds) / rds); // Box-Muller transform
    return x * c; // throw away extra sample y * c
}

var N = 20,
    a = -1,
    b = 1.2;

    var step = (b - a) / (N - 1);
    var t = new Array(N), x = new Array(N), y = new Array(N);

    for(var i = 0; i < N; i++){
        t[i] = a + step * i;
        x[i] = (Math.pow(t[i], 3)) + (0.3 * normal() );
        y[i] = (Math.pow(t[i], 6)) + (0.3 * normal() );
    }

    var trace1 = {
        x: x,
        y: y,
        mode: 'markers',
        name: 'points',
        marker: {
            color: 'rgb(102,0,0)',
            size: 2,
            opacity: 0.4
        },
        type: 'scatter'
    };
    var trace2 = {
        x: x,
        y: y,
        name: 'density',
        ncontours: 20,
        colorscale: 'Hot',
        reversescale: true,
        showscale: false,
        type: 'histogram2dcontour'
    };
    var trace3 = {
        x: x,
        name: 'x density',
        marker: {color: 'rgb(102,0,0)'},
        yaxis: 'y2',
        type: 'histogram'
    };
    var trace4 = {
        y: y,
        name: 'y density',
        marker: {color: 'rgb(102,0,0)'},
        xaxis: 'x2',
        type: 'histogram'
    };
    // var data = [trace1, trace2, trace3, trace4];
    var  data = [trace1, trace2]
    var layout = {
    showlegend: false,
    autosize: false,
    width: 600,
    height: 550,
    margin: {t: 50},
    hovermode: 'closest',
    bargap: 0,
    xaxis: {
        domain: [0, 0.85],
        showgrid: false,
        zeroline: false
    },
    yaxis: {
        domain: [0, 0.85],
        showgrid: false,
        zeroline: false
    },
    // xaxis2: {
    //     domain: [0.85, 1],
    //     showgrid: false,
    //     zeroline: false
    // },
    // yaxis2: {
    //     domain: [0.85, 1],
    //     showgrid: false,
    //     zeroline: false
    // }
};


function TestComp() {
    // Example data
    let newDataset = []
    for (let i = 0 ; i < x.length ; i++) {
        newDataset.push({x:Math.abs(x[i]), y:Math.abs(y[i])})
    }
    const [dataset, setDataset] = useState([
        {x: 10, y: 0},
        {x: 10, y: 10},
        {x: 15, y: 0},
        {x: 15, y: 10},

        {x: 100, y: 0},
        {x: 100, y: 10},
        {x: 105, y: 0},
        {x: 105, y: 10}
        
    ]);
    
    // const [dataset, setDataset] = useState(
    //     newDataset
    // );

    console.log(dataset)


    
    // KDE bandwidth (controls smoothing)
    const bandwidth = 50;  // Adjust this value to change the kernel's spread

    // Resolution (density resolution, e.g., number of density estimates)
    const resolution = 10;  // Adjust for more/less precision
    return (
        <div className="wrapper-Test">
            <NavBarComp/>
            <Typography id="title-Test" variant="h2" component="h1" align="center" sx={{mt: 10, fontWeight: "bold", mb: 10}}>
                Test page
            </Typography>

            <Heatmap data={dataset} bandwidth={bandwidth} resolution={resolution} backgroundImage={minimapImage} />
        </div>
    )
}

export default TestComp