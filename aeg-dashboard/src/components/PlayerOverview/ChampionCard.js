import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { useEffect, useState } from 'react';

import "../../styles/ChampionCard.css"

export default function ChampionCard({championName, pickRate, winRate, nbGames, kda}) {
    const apiURL = `https://ddragon.leagueoflegends.com/cdn/14.5.1/img/champion/${championName}.png`
    const [img, setImg] = useState()

    const fetchImage = async () => {
        const res = await fetch(apiURL)
        const imageBlob = await res.blob()
        const imageObjectURL = URL.createObjectURL(imageBlob);
        setImg(imageObjectURL);
    };

    useEffect(() => {
        fetchImage();
    }, [])

    return (
        <Card 
            sx={{
                maxWidth: 345, 
                ml: 2,
                ':hover': {
                    boxShadow: 20, // theme.shadows[20]
                },
            }}
        >
            <CardMedia
                sx={{height: 140}}
                image={img}
                title={championName}
            />
            <CardContent>
                <Typography gutterBottom variant="h5" component="div">
                    {championName}
                </Typography>
                <Typography variant="body2" color="text.secondary" className='championPool-data'>
                    <p>PickRate : <span>{pickRate}%</span></p>
                    <p>WinRate : <span>{winRate}%</span></p>
                    <p>NbGames : <span>{nbGames}</span></p>
                    <p>KDA : <span>{kda}</span></p>
                </Typography>
            </CardContent>
        </Card>
    )
}