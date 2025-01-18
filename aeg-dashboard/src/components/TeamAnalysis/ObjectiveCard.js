import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';

import GradientTypography from '../utils/GradientTypography';

import "../../styles/ObjectiveCard.css"


export default function ObjectiveCard({objectiveName, objectiveImage, nbGames, nbWin, winRate, media}) {
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
            {
                media ? (
                    <>
                        <CardMedia
                            sx={{height: 140}}
                            image={objectiveImage}
                            title={objectiveName}
                        />
                        <CardContent>
                            <Typography gutterBottom variant="h5" component="div">
                                {objectiveName}
                            </Typography>
                            <Typography variant="body2" color="text.secondary" className='objective-data'>
                                <p>NbGames : <span>{nbGames}</span></p>
                                <p>NbWins : <span>{nbWin}</span></p>
                                <p>WinRate : <span>{winRate}%</span></p>
                                {/* <p>WinRate : <GradientTypography value={winRate} bold={true}>{winRate}%</GradientTypography></p> */}
                            </Typography>
                        </CardContent>
                </>
                ) : (
                    <CardContent>
                        <Typography gutterBottom variant="h5" component="div">
                            {objectiveName}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" className='objective-data'>
                            <p>NbGames : <span>{nbGames}</span></p>
                            <p>NbWins : <span>{nbWin}</span></p>
                            <p>WinRate : <span>{winRate}%</span></p>
                            {/* <p>WinRate : <GradientTypography value={winRate} bold={true}>{winRate}%</GradientTypography></p> */}
                        </Typography>
                    </CardContent>
                )
            }
            
            
        </Card>
    )
}