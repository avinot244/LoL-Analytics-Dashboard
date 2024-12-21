import json
from tqdm import tqdm

from dataAnalysis.packages.Parsers.Separated.Game.SeparatedData import SeparatedData
from dataAnalysis.packages.Parsers.Separated.Game.Snapshot import Snapshot
from dataAnalysis.packages.utils_stuff.utils_func import getData
from dataAnalysis.packages.utils_stuff.Position import Position
from dataAnalysis.packages.AreaMapping.Grid import Grid
from dataAnalysis.packages.AreaMapping.Zone import Zone

from dataAnalysis.packages.utils_stuff.globals import baseBlueBoundaries, baseRedBoundaries

(data, gameDuration, begGameTime, endGameTime) = getData(2729017, 5)
print(gameDuration, begGameTime, endGameTime)

# for snapshot in data.gameSnapshotList:
#     current_time : float = snapshot.convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime)
gridBlueBase : Grid = Grid([Zone(baseBlueBoundaries)])
gridRedBase : Grid = Grid([Zone(baseRedBoundaries)])
result : dict = {
    "blueTeam": {},
    "redTeam": {}
}

firstSnapshot : Snapshot = data.gameSnapshotList[0]
for player in firstSnapshot.teams[0].players:
    result["blueTeam"][player.playerName] = []

for player in firstSnapshot.teams[1].players:
    result["redTeam"][player.playerName] = []



def didPlayerReset(playerName : str, dataWindow : list[Snapshot], team : int):
    participantID : int = dataWindow[0].teams[team].getPlayerID(playerName)
    playerIdx : int = dataWindow[0].teams[team].getPlayerIdx(participantID)
    positionFirstSecond : Position = dataWindow[0].teams[team].getPlayerPosition(playerIdx)
    positionSecondSecond : Position = dataWindow[1].teams[team].getPlayerPosition(playerIdx)
    
    if team == 0:
        return not(gridBlueBase.containsPoint(positionFirstSecond)) and gridBlueBase.containsPoint(positionSecondSecond)
    elif team == 1:
        return not(gridRedBase.containsPoint(positionFirstSecond)) and gridRedBase.containsPoint(positionSecondSecond)

for time in tqdm(range(120, gameDuration + 1)):
    currentSnapshot : Snapshot = data.getSnapShotByTime(time, gameDuration)
    dataWindow : list[Snapshot] = [data.getSnapShotByTime(t, gameDuration) for t in range(time, time+2, 1)]
    
    for player in currentSnapshot.teams[0].players:
        if didPlayerReset(player.playerName, dataWindow, 0):
            result["blueTeam"][player.playerName].append({
                "time": time,
                "position": player.position.__dict__
            })
            
    for player in currentSnapshot.teams[1].players:
        if didPlayerReset(player.playerName, dataWindow, 1):
            result["redTeam"][player.playerName].append({
                "time": time,
                "position": player.position.__dict__
            })

print(json.dumps(result, indent=4))