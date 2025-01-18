import ObjectiveCard from "./ObjectiveCard"

import { Stack } from "@mui/material"

function TeamAnalysisOverallData ({dataGrubsDrakes, dataFirstTowerHerald, dataHerald, dataFirstTower}) {
    return (
        <div className="teamAnalysisOverallData">
            <Stack direction={"row"} spacing={5} justifyContent="center" alignItems="center" sx={{mt: 5}}>
                <ObjectiveCard 
                    objectiveName={"First Tower Winrate"}
                    nbGames={dataFirstTower.totalGames}
                    winRate={(dataFirstTower.winRate*100).toFixed(2)}
                    nbWin={dataFirstTower.totalWins}
                    media={false}
                />

                <ObjectiveCard 
                    objectiveName={"Herald Winrate"}
                    nbGames={dataHerald.totalGames}
                    winRate={(dataHerald.winRate*100).toFixed(2)}
                    nbWin={dataHerald.totalWins}
                    media={false}
                />

                <ObjectiveCard
                    objectiveName={"Herald over First Tower Winrate"}
                    nbGames={dataFirstTowerHerald.totalGames}
                    winRate={(dataFirstTowerHerald.winRate*100).toFixed(2)}
                    nbWin={dataFirstTowerHerald.totalWins}
                    media={false}
                />
            </Stack>
        </div>
    )
}

export default TeamAnalysisOverallData