import { useEffect, useState } from "react"
import { API_URL } from "../../constants"
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { FormControlLabel, FormGroup, Switch } from "@mui/material";
import { Line } from 'react-chartjs-2';
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

export default function GameOverviewStat({seriesId, gameNumber}) {
    const [dataGamePlayer, setDataGamePlayer] = useState({})
    const [labels, setLabels] = useState([])

    const [displayDPM, setDisplayDPM] = useState(true)
    const [displayCurrentGold, setDisplayCurrentGold] = useState(false)
    const [displayGPM, setDisplayGPM] = useState(false)
    const [displayXPM, setDisplayXPM] = useState(false)
    const [displayCSM, setDisplayCSM] = useState(false)

    const [displayTeamBlue, setDisplayTeamBlue] = useState(true)
    const [displayTeamRed, setDisplayTeamRed] = useState(false)

    useEffect(() => {
        const fetchGameDataPlayer = async (seriesId, gameNumber) => {
            const result = await fetch(API_URL + `dataAnalysis/gameAnalysis/players/${seriesId}/${gameNumber}/`, {
                method: "GET"
            })

            result.json().then(result => {
                const newData = result.data
                console.log("data :", newData)
                setDataGamePlayer(newData)

                let newLabels = []
                for (let i = 0 ; i < result.gameLength + 1 ; i++) {
                    newLabels.push(i)
                }
                setLabels(newLabels)
            })
        }

        fetchGameDataPlayer(seriesId, gameNumber)

        
        
    }, [])

    let datasets = []
    
    for (let i = 0 ; i < dataGamePlayer.length ; i++) {
        let playerObject = dataGamePlayer[i]
        let tempDPM = {
            label: `DPM ${playerObject.playerName}`,
            data: playerObject.DPM,
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
            hidden: !(displayDPM && ((displayTeamBlue && i < 5) || (displayTeamRed && i > 4)))
        }
        datasets.push(tempDPM)
        let tempCurrentGold = {
            label: `Current Gold ${playerObject.playerName}`,
            data: playerObject.currentGold,
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
            hidden: !(displayCurrentGold && ((displayTeamBlue && i < 5) || (displayTeamRed && i > 4)))
        }
        datasets.push(tempCurrentGold)
        let tempGPM = {
            label: `GPM ${playerObject.playerName}`,
            data: playerObject.GPM,
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
            hidden: !(displayGPM && ((displayTeamBlue && i < 5) || (displayTeamRed && i > 4)))
        }
        datasets.push(tempGPM)
        let tempXPM = {
            label: `GPM ${playerObject.playerName}`,
            data: playerObject.XPM,
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
            hidden: !(displayXPM && ((displayTeamBlue && i < 5) || (displayTeamRed && i > 4)))
        }
        datasets.push(tempXPM)
        let tempCSM = {
            label: `XPM ${playerObject.playerName}`,
            data: playerObject.CSM,
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
            hidden: !(displayCSM && ((displayTeamBlue && i < 5) || (displayTeamRed && i > 4)))
        }
        datasets.push(tempCSM)
    }

    console.log("datasets :", datasets)

    const dataPlayer = {
        labels,
        datasets: datasets
    }

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: "Stat evolution players"
            }
        }
    }

    return (
        <>
            <FormGroup row>
                <FormControlLabel control={<Switch defaultChecked onChange={(event) => {setDisplayDPM(event.target.checked)}}/>} label={`DPM`}/>
                <FormControlLabel control={<Switch onChange={(event) => {setDisplayCurrentGold(event.target.checked)}}/>} label={`Current Gold`}/>
                <FormControlLabel control={<Switch onChange={(event) => {setDisplayGPM(event.target.checked)}}/>} label={`GPM`}/>
                <FormControlLabel control={<Switch onChange={(event) => {setDisplayXPM(event.target.checked)}}/>} label={`XPM`}/>
                <FormControlLabel control={<Switch onChange={(event) => {setDisplayCSM(event.target.checked)}}/>} label={`CSM`}/>

            </FormGroup>

            <FormGroup row>
                <FormControlLabel control={<Switch defaultChecked onChange={(event) => {setDisplayTeamBlue(event.target.checked)}}/>} label={`Team Blue`}/>
                <FormControlLabel control={<Switch onChange={(event) => {setDisplayTeamRed(event.target.checked)}}/>} label={`Team Red`}/>
            </FormGroup>

            <Line options={options} data={dataPlayer}/>
        </>
        
    )
}