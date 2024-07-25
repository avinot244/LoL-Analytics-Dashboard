import { useState, useContext, useEffect } from "react"

import { Button, Stack, Typography } from "@mui/material"

import AuthContext from "../context/AuthContext"
import { API_URL } from "../../constants"

function PlayerOverviewDensity({summonnerName, patch, tournament, limit}){
    // React useStates for position density images for red side
    const [densityTournamentRed, setDensityTournamentRed] = useState()
    const [densityPatchRed, setDensityPatchRed] = useState()
    const [densityLimitRed, setDensityLimitRed] = useState()
    // React useStates for position density images for blue side
    const [densityTournamentBlue, setDensityTournamentBlue] = useState()
    const [densityPatchBlue, setDensityPatchBlue] = useState()
    const [densityLimitBlue, setDensityLimitBlue] = useState()

    const [loading, setLoading] = useState(true)

    // Getting authcontext and headers
    let {authTokens} = useContext(AuthContext)
    const header = {
        Authorization: "Bearer " + authTokens.access
    }

    // Fetch method to get player density for tournament
    const fetchDensityTournament = async (tournament, summonnerName, side) => {
        setLoading(false)
        const res = await fetch(API_URL + `dataAnalysis/playerDensityTournament/${tournament}/${summonnerName}/840/${side}/`, {
            method: "GET",
            headers: header
        })
        if (res.status === 200) {
            const imageBlob = await res.blob()
            const imageObjectURL = URL.createObjectURL(imageBlob)
            if (side === "Red") {
                setDensityTournamentRed(imageObjectURL)
                setLoading(true)
            }else if (side === "Blue") {
                setDensityTournamentBlue(imageObjectURL)
                setLoading(true)
            }
        }
    }
    // Fetch method to get player density for patch
    const fetchDensityPatch = async (patch, summonnerName, side) => {
        setLoading(false)
        const res = await fetch(API_URL + `dataAnalysis/playerDensityPatch/${patch}/${summonnerName}/840/${side}/`, {
            method: "GET",
            headers: header
        })
        if (res.status === 200) {
            const imageBlob = await res.blob()
            const imageObjectURL = URL.createObjectURL(imageBlob)
            if (side === "Red") {
                setDensityPatchRed(imageObjectURL)
                setLoading(true)
            }else if (side === "Blue") {
                setDensityPatchBlue(imageObjectURL)
                setLoading(true)
            }
        }
    }
    // Fetch method to get player density for latest ${limit} games
    const fetchDensityLatest = async (patch, tournament, limit, summonnerName, side) => {
        setLoading(false)
        const res = await fetch(API_URL + `dataAnalysis/playerDensityPatch/${patch}/${tournament}/${limit}/${summonnerName}/840/${side}/`, {
            method: "GET",
            headers: header
        })
        if (res.status === 200) {
            const imageBlob = await res.blob()
            const imageObjectURL = URL.createObjectURL(imageBlob)
            if (side === "Red") {
                setDensityLimitRed(imageObjectURL)
                setLoading(true)
            } else if (side === "Blue") {
                setDensityLimitBlue(imageObjectURL)
                setLoading(true)
            }
        }
    }

    return (
        <div className="playerOverview-position-density">
            <div className="playerOverview-position-density-tournament">
                <Stack spacing={2} direction="row" justifyContent="center" alignItems="center">
                    {
                        loading ? (
                            <Button
                                variant="contained"
                                onClick={() => {
                                    fetchDensityTournament(tournament, summonnerName, "Blue")  
                                }}
                            >
                                Get Density tournament Blue
                            </Button>
                        ) : (
                            <Button
                                variant="disabled"
                            >
                                Get Density tournament Blue
                            </Button>
                        )
                        
                    }

                    {
                        loading ? (
                            <Button
                                variant="contained"
                                onClick={() => {
                                    fetchDensityTournament(tournament, summonnerName, "Red")
                                }}
                            >
                                Get Density tournament Red
                            </Button>
                        ) : (
                            <Button 
                                variant="disabled"
                            >
                                Get Density tournament Red
                            </Button>
                        )
                        
                    }
                </Stack>
                
                <Typography id="title-density-tournament" variant="h6" component="h2" align="center">
                    Position Density {tournament}
                </Typography>
                <Stack spacing={2} direction="row" justifyContent="center" alignItems="center">
                    <img src={densityTournamentBlue} alt="density-player-tournament-blue" width={480}/>
                    <img src={densityTournamentRed} alt="density-player-tournament-red" width={480}/>
                </Stack>
            </div>
            
            <div className="playerOverview-position-density-tournament">
                <Stack spacing={2} direction="row" justifyContent="center" alignItems="center">
                    {
                        loading ? (
                            <Button
                                variant="contained"
                                onClick={() => {
                                    fetchDensityPatch(patch, summonnerName, "Blue")  
                                }}
                            >
                                Get Density patch Blue
                            </Button>
                        ) : (
                            <Button
                                variant="disabled"
                            >
                                Get Density patch Blue
                            </Button>
                        )
                        
                    }

                    {
                        loading ? (
                            <Button
                                variant="contained"
                                onClick={() => {
                                    fetchDensityPatch(patch, summonnerName, "Red")
                                }}
                            >
                                Get Density patch Red
                            </Button>
                        ) : (
                            <Button 
                                variant="disabled"
                            >
                                Get Density patch Red
                            </Button>
                        )
                        
                    }
                </Stack>
                <Typography id="title-density-patch" variant="h6" component="h2" align="center">
                    Position Density {patch}
                </Typography>
                <Stack spacing={2} direction="row" justifyContent="center" alignItems="center">
                    <img src={densityPatchRed} alt="density-player-patch-red" width={480}/>
                    <img src={densityPatchBlue} alt="density-player-patch-red" width={480}/>
                </Stack> 
            </div>
            
            <div className="playerOverview-position-density-latest">
                <Stack spacing={2} direction="row" justifyContent="center" alignItems="center">
                    {
                        loading ? (
                            <Button
                                variant="contained"
                                onClick={() => {
                                    fetchDensityLatest(patch, tournament, limit, summonnerName, "Blue")  
                                }}
                            >
                                Get Density latest {limit} Blue
                            </Button>
                        ) : (
                            <Button
                                variant="disabled"
                            >
                                Get Density patch {limit} Blue
                            </Button>
                        )
                    }

                    {
                        loading ? (
                            <Button
                                variant="contained"
                                onClick={() => {
                                    fetchDensityLatest(patch, tournament, limit, summonnerName, "Red")  
                                }}
                            >
                                Get Density latest {limit} Red
                            </Button>
                        ) : (
                            <Button
                                variant="disabled"
                            >
                                Get Density patch {limit} Red
                            </Button>
                        )
                    }
                </Stack>
                <Typography id="title-density-latest" variant="h6" component="h2" align="center">
                    Position Density Latest {limit}
                </Typography>
                <Stack spacing={2} direction="row" justifyContent="center" alignItems="center">
                    <img src={densityLimitRed} alt="density-player-latest-red" width={480}/>
                    <img src={densityLimitBlue} alt="density-player-latest-red" width={480}/>
                </Stack> 
            </div>
            
        </div>
    )
}

export default PlayerOverviewDensity