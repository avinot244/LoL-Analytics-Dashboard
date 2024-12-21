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
splitList : list[int] = [120, 840]
splittedData : list[SeparatedData] = data.splitData(gameDuration, splitList)

print(len(splittedData))
for data in splittedData:
    print(max([snap.convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime) for snap in data.gameSnapshotList]))
    