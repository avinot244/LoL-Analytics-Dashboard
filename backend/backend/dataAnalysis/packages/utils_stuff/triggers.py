from dataAnalysis.packages.Parsers.Separated.Game.Snapshot import Snapshot
from dataAnalysis.packages.utils_stuff.Position import Position
from dataAnalysis.packages.AreaMapping.Grid import Grid
from dataAnalysis.packages.AreaMapping.Zone import Zone

from dataAnalysis.packages.utils_stuff.globals import baseBlueBoundaries, baseRedBoundaries

def didPlayerReset(playerName : str, dataWindow : list[Snapshot], team : int):
    gridBlueBase : Grid = Grid([Zone(baseBlueBoundaries)])
    gridRedBase : Grid = Grid([Zone(baseRedBoundaries)])
    
    participantID : int = dataWindow[0].teams[team].getPlayerID(playerName)
    playerIdx : int = dataWindow[0].teams[team].getPlayerIdx(participantID)
    positionFirstSecond : Position = dataWindow[0].teams[team].getPlayerPosition(playerIdx)
    positionSecondSecond : Position = dataWindow[1].teams[team].getPlayerPosition(playerIdx)
    
    if team == 0:
        return not(gridBlueBase.containsPoint(positionFirstSecond)) and gridBlueBase.containsPoint(positionSecondSecond)
    elif team == 1:
        return not(gridRedBase.containsPoint(positionFirstSecond)) and gridRedBase.containsPoint(positionSecondSecond)
    
def didPlayerTP(playerName : str):
    pass