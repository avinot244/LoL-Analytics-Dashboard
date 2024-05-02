import { useEffect, useState } from "react"
import { API_URL } from "../../constants"
import "../../styles/GameOverviewStat.css"
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
import { FormControlLabel, FormGroup, Switch} from "@mui/material";
import { alpha, styled } from '@mui/material/styles';
import { blue, teal, red, yellow, purple } from '@mui/material/colors';
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


const BlueSwitch = styled(Switch)(({ theme }) => ({
    '& .MuiSwitch-switchBase.Mui-checked': {
        color: blue[600],
        '&:hover': {
            backgroundColor: alpha(blue[600], theme.palette.action.hoverOpacity),
        },
    },
    '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
        backgroundColor: blue[600],
    },
}));

const TealSwitch = styled(Switch)(({ theme }) => ({
    '& .MuiSwitch-switchBase.Mui-checked': {
        color: teal[600],
        '&:hover': {
            backgroundColor: alpha(teal[600], theme.palette.action.hoverOpacity),
        },
    },
    '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
        backgroundColor: teal[600],
    },
}));

const RedSwitch = styled(Switch)(({ theme }) => ({
    '& .MuiSwitch-switchBase.Mui-checked': {
        color: red[600],
        '&:hover': {
            backgroundColor: alpha(red[600], theme.palette.action.hoverOpacity),
        },
    },
    '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
        backgroundColor: red[600],
    },
}));

const YellowSwitch = styled(Switch)(({ theme }) => ({
    '& .MuiSwitch-switchBase.Mui-checked': {
        color: yellow[600],
        '&:hover': {
            backgroundColor: alpha(yellow[600], theme.palette.action.hoverOpacity),
        },
    },
    '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
        backgroundColor: yellow[600],
    },
}));

const PurpleSwitch = styled(Switch)(({ theme }) => ({
    '& .MuiSwitch-switchBase.Mui-checked': {
        color: purple[600],
        '&:hover': {
            backgroundColor: alpha(purple[600], theme.palette.action.hoverOpacity),
        },
    },
    '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
        backgroundColor: purple[600],
    },
}));

export default function GameOverviewStat({seriesId, gameNumber}) {
    const [dataGamePlayer, setDataGamePlayer] = useState([])
    const [dataGameTeams, setDataGameTeams] = useState([])
    const [labels, setLabels] = useState([])

    const [displayDPM, setDisplayDPM] = useState(true)
    const [displayCurrentGold, setDisplayCurrentGold] = useState(false)
    const [displayGPM, setDisplayGPM] = useState(false)
    const [displayXPM, setDisplayXPM] = useState(false)
    const [displayCSM, setDisplayCSM] = useState(false)

    const [displayTeamBluePlayer, setDisplayTeamBluePlayer] = useState(true)
    const [displayTeamRedPlayer, setDisplayTeamRedPlayer] = useState(false)


    const [displayTeamBlue, setDisplayTeamBlue] = useState(true)
    const [displayTeamRed, setDisplayTeamRed] = useState(false)

    const [displayDPMTeam, setDisplayDPMTeam] = useState(true)
    const [displayCurrentGoldTeam, setDisplayCurrentGoldTeam] = useState(false)
    const [displayGPMTeam, setDisplayGPMTeam] = useState(false)
    const [displayXPMTeam, setDisplayXPMTeam] = useState(false)
    const [displayCSMTeam, setDisplayCSMTeam] = useState(false)



    const [displayTopRed, setDisplayTopRed] = useState(true)
    const [displayJungleRed, setDisplayJungleRed] = useState(true)
    const [displayMidRed, setDisplayMidRed] = useState(true)
    const [displayADCRed, setDisplayADCRed] = useState(true)
    const [displaySupportRed, setDisplaySupportRed] = useState(true)

    const [displayTopBlue, setDisplayTopBlue] = useState(true)
    const [displayJungleBlue, setDisplayJungleBlue] = useState(true)
    const [displayMidBlue, setDisplayMidBlue] = useState(true)
    const [displayADCBlue, setDisplayADCBlue] = useState(true)
    const [displaySupportBlue, setDisplaySupportBlue] = useState(true)

    
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

        const fetchGameDataTeams = async (seriesId, gameNumber) => {
            const result = await fetch(API_URL + `dataAnalysis/gameAnalysis/teams/${seriesId}/${gameNumber}/`, {
                method: "GET"
            })

            result.json().then(result => {
                const newData = result.data
                setDataGameTeams(newData)

                let newLabels = []
                for (let i = 0 ; i < result.gameLength + 1 ; i++) {
                    newLabels.push(i)
                }
                setLabels(newLabels)
            })
        }

        fetchGameDataPlayer(seriesId, gameNumber)
        fetchGameDataTeams(seriesId, gameNumber)
    }, [])


    let datasetsPlayer = []
    let colorList = [
        {
            "borderColor": "rgb(65, 159, 235)",
            "backgroundColor": "rgba(65, 159, 235, 0.5)"
        },
        {
            "borderColor": "rgb(74, 191, 192)",
            "backgroundColor": "rgba(74, 191, 192, 0.5)"
        },
        {
            "borderColor": "rgb(255, 99, 132)",
            "backgroundColor": "rgba(255, 99, 132, 0.5)"
        },
        {
            "borderColor": "rgb(253, 208, 87)",
            "backgroundColor": "rgba(253, 208, 87, 0.5)"
        },
        {
            "borderColor": "rgb(160, 94, 254)",
            "backgroundColor": "rgba(160, 94, 254, 0.5)"
        },
        {
            "borderColor": "rgb(65, 159, 235)",
            "backgroundColor": "rgba(65, 159, 235, 0.5)"
        },
        {
            "borderColor": "rgb(74, 191, 192)",
            "backgroundColor": "rgba(74, 191, 192, 0.5)"
        },
        {
            "borderColor": "rgb(255, 99, 132)",
            "backgroundColor": "rgba(255, 99, 132, 0.5)"
        },
        {
            "borderColor": "rgb(253, 208, 87)",
            "backgroundColor": "rgba(253, 208, 87, 0.5)"
        },
        {
            "borderColor": "rgb(160, 94, 254)",
            "backgroundColor": "rgba(160, 94, 254, 0.5)"
        }
    ]
    let pointStyle = ["circle", "circle", "circle", "circle", "circle", "crossRot", "crossRot", "crossRot", "crossRot", "crossRot"]
    for (let i = 0 ; i < dataGamePlayer.length ; i++) {
        let playerObject = dataGamePlayer[i]
        let displayRoleBlue = (displayTopBlue && i === 0) || (displayJungleBlue && i === 1) || (displayMidBlue && i === 2) || (displayADCBlue && i === 3) || (displaySupportBlue && i === 4) 
        let displayRoleRed = (displayTopRed && i === 5) || (displayJungleRed && i === 6) || (displayMidRed && i === 7) || (displayADCRed && i === 8) || (displaySupportRed && i === 9)

        
        let tempDPM = {
            label: `DPM ${playerObject.playerName}`,
            data: playerObject.DPM,
            borderColor: colorList[i].borderColor,
            backgroundColor: colorList[i].backgroundColor,
            pointStyle: pointStyle[i],
            borderWidth: 1,
            hidden: !(displayDPM && (displayRoleBlue || displayRoleRed))
        }
        datasetsPlayer.push(tempDPM)
        let tempCurrentGold = {
            label: `Current Gold ${playerObject.playerName}`,
            data: playerObject.currentGold,
            borderColor: colorList[i].borderColor,
            backgroundColor: colorList[i].backgroundColor,
            pointStyle: pointStyle[i],
            borderWidth: 1,
            hidden: !(displayCurrentGold && (displayRoleBlue || displayRoleRed))
        }
        datasetsPlayer.push(tempCurrentGold)
        let tempGPM = {
            label: `GPM ${playerObject.playerName}`,
            data: playerObject.GPM,
            borderColor: colorList[i].borderColor,
            backgroundColor: colorList[i].backgroundColor,
            pointStyle: pointStyle[i],
            borderWidth: 1,
            hidden: !(displayGPM && (displayRoleBlue || displayRoleRed))
        }
        datasetsPlayer.push(tempGPM)
        let tempXPM = {
            label: `XPM ${playerObject.playerName}`,
            data: playerObject.XPM,
            borderColor: colorList[i].borderColor,
            backgroundColor: colorList[i].backgroundColor,
            pointStyle: pointStyle[i],
            borderWidth: 1,
            hidden: !(displayXPM && (displayRoleBlue || displayRoleRed))
        }
        datasetsPlayer.push(tempXPM)
        let tempCSM = {
            label: `CPM ${playerObject.playerName}`,
            data: playerObject.CSM,
            borderColor: colorList[i].borderColor,
            backgroundColor: colorList[i].backgroundColor,
            pointStyle: pointStyle[i],
            borderWidth: 1,
            hidden: !(displayCSM && (displayRoleBlue || displayRoleRed))
        }
        datasetsPlayer.push(tempCSM)
    }
    const dataPlayer = {
        labels,
        datasets: datasetsPlayer
    }
    const optionsPlayer = {
        responsive: true,
        plugins: {
            legend: {
                display: false,
                labels: {
                    usePointStyle: true,
                }
            },
            title: {
                display: true,
                text: "Stat evolution players"
            }
        }
    }

    let colorListTeams = [
        {
            "backgroundColor": 'rgba(54, 162, 235, 0.2)',
            "borderColor": 'rgb(54, 162, 235)',
        },
        {
            "borderColor": 'rgb(255, 99, 132)',
            "backgroundColor": 'rgba(255, 99, 132, 0.2)'
        }
    ]
    let pointStyleTeam = ["circle", "crossRot"]
    let datasetsTeams = []
    for (let i = 0 ; i < dataGameTeams.length ; i++) {
        let teamObject = dataGameTeams[i]
        let displayTeam = ((displayTeamBlue && teamObject.teamSide === "Blue") || (displayTeamRed && teamObject.teamSide === "Red"))
        
        let tempDPM = {
            label: `Team ${teamObject.teamSide} DPM`,
            data: teamObject.DPM,
            borderColor: colorListTeams[i]["borderColor"],
            backgroundColor: colorListTeams[i]["backgroundColor"],
            hidden: !(displayDPMTeam && displayTeam),
            pointStyle: pointStyleTeam[i],
            borderWidth: 1,
        }
        datasetsTeams.push(tempDPM)

        let tempCurrentGold = {
            label: `Team ${teamObject.teamSide} Current Gold`,
            data: teamObject.currentGold,
            borderColor: colorListTeams[i]["borderColor"],
            backgroundColor: colorListTeams[i]["backgroundColor"],
            hidden: !(displayCurrentGoldTeam && displayTeam),
            pointStyle: pointStyleTeam[i],
            borderWidth: 1,
        }
        datasetsTeams.push(tempCurrentGold)

        let tempGPM = {
            label: `Team ${teamObject.teamSide} GPM`,
            data: teamObject.GPM,
            borderColor: colorListTeams[i]["borderColor"],
            backgroundColor: colorListTeams[i]["backgroundColor"],
            hidden: !(displayGPMTeam && displayTeam),
            pointStyle: pointStyleTeam[i],
            borderWidth: 1,
        }
        datasetsTeams.push(tempGPM)

        let tempXPM = {
            label: `Team ${teamObject.teamSide} XPM`,
            data: teamObject.XPM,
            borderColor: colorListTeams[i]["borderColor"],
            backgroundColor: colorListTeams[i]["backgroundColor"],
            hidden: !(displayXPMTeam && displayTeam),
            pointStyle: pointStyleTeam[i],
            borderWidth: 1,
        }
        datasetsTeams.push(tempXPM)

        let tempCSM = {
            label: `Team ${teamObject.teamSide} CSM`,
            data: teamObject.CSM,
            borderColor: colorListTeams[i]["borderColor"],
            backgroundColor: colorListTeams[i]["backgroundColor"],
            hidden: !(displayCSMTeam && displayTeam),
            pointStyle: pointStyleTeam[i],
            borderWidth: 1,
        }
        datasetsTeams.push(tempCSM)
    }
    const dataTeam = {
        labels,
        datasets: datasetsTeams
    }
    const optionsTeam = {
        responsive: true,
        plugins: {
            legend: {
                display: false,
                labels: {
                    usePointStyle: true,
                }
            },
            title: {
                display: true,
                text: "Stat evolution teams"
            }
        }
    }
    

    
    
    return (
        <div className="wrapper-charts-GameOverviewStat">
            <br/>
            <div className="charts">
                <div className="chart-team">
                    <FormGroup row>
                        <FormControlLabel control={<Switch defaultChecked onChange={(event) => {setDisplayDPMTeam(event.target.checked)}}/>} label={`DPM`}/>
                        <FormControlLabel control={<Switch onChange={(event) => {setDisplayCurrentGoldTeam(event.target.checked)}}/>} label={`Current Gold`}/>
                        <FormControlLabel control={<Switch onChange={(event) => {setDisplayGPMTeam(event.target.checked)}}/>} label={`GPM`}/>
                        <FormControlLabel control={<Switch onChange={(event) => {setDisplayXPMTeam(event.target.checked)}}/>} label={`XPM`}/>
                        <FormControlLabel control={<Switch onChange={(event) => {setDisplayCSMTeam(event.target.checked)}}/>} label={`CSM`}/>
                    </FormGroup>
                    <FormGroup row>
                        <FormControlLabel control={<Switch defaultChecked onChange={(event) => {setDisplayTeamBlue(event.target.checked)}}/>} label={`Team Blue o`}/>
                        <FormControlLabel control={<RedSwitch onChange={(event) => {setDisplayTeamRed(event.target.checked)}}/>} label={`Team Red x`}/>
                    </FormGroup>
                    <Line options={optionsTeam} data={dataTeam}/>
                    
                </div> 
                <div className="chart-player">
                    <FormGroup row>
                        <FormControlLabel control={<Switch defaultChecked onChange={(event) => {setDisplayDPM(event.target.checked)}}/>} label={`DPM`}/>
                        <FormControlLabel control={<Switch onChange={(event) => {setDisplayCurrentGold(event.target.checked)}}/>} label={`Current Gold`}/>
                        <FormControlLabel control={<Switch onChange={(event) => {setDisplayGPM(event.target.checked)}}/>} label={`GPM`}/>
                        <FormControlLabel control={<Switch onChange={(event) => {setDisplayXPM(event.target.checked)}}/>} label={`XPM`}/>
                        <FormControlLabel control={<Switch onChange={(event) => {setDisplayCSM(event.target.checked)}}/>} label={`CSM`}/>
                    </FormGroup>

                    <FormGroup row>
                        <FormControlLabel control={<BlueSwitch defaultChecked onChange={(event) => {setDisplayTopBlue(event.target.checked)}}/>} label={`Top o`} color=""/>
                        <FormControlLabel control={<TealSwitch defaultChecked onChange={(event) => {setDisplayJungleBlue(event.target.checked)}}/>} label={`Jungle o`}/>
                        <FormControlLabel control={<RedSwitch defaultChecked onChange={(event) => {setDisplayMidBlue(event.target.checked)}}/>} label={`Mid o`}/>
                        <FormControlLabel control={<YellowSwitch defaultChecked onChange={(event) => {setDisplayADCBlue(event.target.checked)}}/>} label={`ADC o`}/>
                        <FormControlLabel control={<PurpleSwitch defaultChecked onChange={(event) => {setDisplaySupportBlue(event.target.checked)}}/>} label={`Support o`}/>
                    </FormGroup>

                    <FormGroup row>
                        <FormControlLabel control={<BlueSwitch defaultChecked onChange={(event) => {setDisplayTopRed(event.target.checked)}}/>} label={`Top x`} color=""/>
                        <FormControlLabel control={<TealSwitch defaultChecked onChange={(event) => {setDisplayJungleRed(event.target.checked)}}/>} label={`Jungle x`}/>
                        <FormControlLabel control={<RedSwitch defaultChecked onChange={(event) => {setDisplayMidRed(event.target.checked)}}/>} label={`Mid x`}/>
                        <FormControlLabel control={<YellowSwitch defaultChecked onChange={(event) => {setDisplayADCRed(event.target.checked)}}/>} label={`ADC x`}/>
                        <FormControlLabel control={<PurpleSwitch defaultChecked onChange={(event) => {setDisplaySupportRed(event.target.checked)}}/>} label={`Support x`}/>
                    </FormGroup>
                    <Line options={optionsPlayer} data={dataPlayer}/>
                </div>
            </div>
        </div>
    )
}
