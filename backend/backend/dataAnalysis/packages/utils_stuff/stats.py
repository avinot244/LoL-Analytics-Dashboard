import csv

from dataAnalysis.packages.Parsers.Separated.Game.Snapshot import Snapshot
from dataAnalysis.packages.Parsers.Separated.Game.SeparatedData import SeparatedData
from dataAnalysis.packages.Parsers.Separated.Game.Player import Player
from dataAnalysis.packages.utils_stuff.globals import *
from dataAnalysis.packages.GameStat import GameStat


def saveDiffStatGame(stat : GameStat, path : str, snapShot : Snapshot):
    teamOneName = snapShot.teams[0].getTeamName()
    teamTwoName = snapShot.teams[1].getTeamName()

    csv_name = "{}diff_{}_{}_against_{}.csv".format(path, stat.time, teamOneName, teamTwoName)

    with open(csv_name, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        header =  ["Player_Name", "XPD@{}".format(stat.time), "CSD@{}".format(stat.time), "GD@{}".format(stat.time)]
        writer.writerow(header)
        for i in range(5):
            data = []
            data.append(snapShot.teams[0].players[i].playerName)
            data.append(stat.playerXPDiff[i])
            data.append(stat.playerCSDiff[i])
            data.append(stat.playerGoldDiff[i])
            writer.writerow(data)
              

def saveDiffStatBO(statList : list[GameStat], path : str, snapShotList : list[Snapshot]):
    teamOneName = snapShotList[0].teams[0].getTeamName()
    teamTwoName = snapShotList[0].teams[1].getTeamName()
    timeSaved = statList[0].time

    csv_name = "{}/diff_{}_{}_against_{}.csv".format(path, timeSaved, teamOneName, teamTwoName)
    
    with open(csv_name, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        header = ['Player_Name', 'XPD@{}'.format(timeSaved), 'CSD@{}'.format(timeSaved), 'GD@{}'.format(timeSaved)]
        writer.writerow(header)

        playerXPDiffAvg : list[float] = list()
        playerCSDiffAvg : list[float] = list()
        playerGoldDiffAvg : list[float] = list()

        for i in range(5):
            XPDiffAvg : float = 0
            CSDiffAvg : float = 0
            GoldDiffAvg : float = 0
            for stat in statList:
                XPDiffAvg += stat.playerXPDiff[i]
                CSDiffAvg += stat.playerCSDiff[i]
                GoldDiffAvg += stat.playerGoldDiff[i]
            playerXPDiffAvg.append(XPDiffAvg/len(statList))
            playerCSDiffAvg.append(CSDiffAvg/len(statList))
            playerGoldDiffAvg.append(GoldDiffAvg/len(statList))

            data = []
            data.append(snapShotList[0].teams[0].players[i].playerName)
            data.append(playerXPDiffAvg[i])
            data.append(playerCSDiffAvg[i])
            data.append(playerGoldDiffAvg[i])
            writer.writerow(data)

            
def getJungleProximity(data : SeparatedData, team : int):
    """team attribute stands for the number of the team (can be either zero or one)"""
    jungleProximitySummary : dict = dict()
    
    if team == 0:
        playerList = data.gameSnapshotList[0].teams[0].getPlayerList()
        for playerName in playerList:
            jungleProximitySummary[playerName] = 0
    elif team == 1:
        playerList = data.gameSnapshotList[0].teams[1].getPlayerList()
        for playerName in playerList:
            jungleProximitySummary[playerName] = 0
    
    c = 0
    for snapshot in data.gameSnapshotList:
        if team == 0:
            closestPlayer : Player = snapshot.teams[0].getClosesPlayerToJungler()
            jungleProximitySummary[closestPlayer.playerName] += 1
        elif team == 1:
            closestPlayer : Player = snapshot.teams[1].getClosesPlayerToJungler()
            jungleProximitySummary[closestPlayer.playerName] += 1
        c += 1
    
    for k in jungleProximitySummary.keys():
        jungleProximitySummary[k] /= c
    
    return jungleProximitySummary

def getProxomityMatrix(data : SeparatedData, team : int):
    proximityMatrix : list[list] = list()
    for _ in range(5):
        proximityMatrix.append([0, 0, 0, 0, 0])
    
    for snapshot in data.gameSnapshotList:
        for indexPlayer in range(5):
            player : Player = snapshot.teams[team].players[indexPlayer]
            indexClosestPlayer : int = snapshot.teams[team].getPlayerIdx(snapshot.teams[team].getClosestPlayer(player).participantID)
            proximityMatrix[indexPlayer][indexClosestPlayer] += 1
    for i in range(len(proximityMatrix)):
        for j in range(len(proximityMatrix)):
            proximityMatrix[i][j] /= len(data.gameSnapshotList)
    
    # Setting the diagonal to 1 because a given player is the closest to himself at any time
    for i in range(len(proximityMatrix)):
        for j in range(len(proximityMatrix)):
            if i==j:
                proximityMatrix[i][j] = 1

    return proximityMatrix


