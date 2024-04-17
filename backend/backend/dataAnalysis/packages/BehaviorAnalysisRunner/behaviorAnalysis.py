from dataAnalysis.packages.AreaMapping.AreaMapping import AreaMapping
from dataAnalysis.packages.GameStat import GameStat
from dataAnalysis.packages.Parsers.Separated.Game.SeparatedData import SeparatedData
from dataAnalysis.packages.Parsers.Separated.Game.Snapshot import Snapshot
from dataAnalysis.packages.Parsers.Separated.Game.Stat import Stat
from dataAnalysis.packages.utils_stuff.stats import getJungleProximity
from dataAnalysis.packages.utils_stuff.globals import roleMap

from dataAnalysis.packages.utils_stuff.utils_func import isInDataBase


import pandas as pd


import csv

def getBehaviorData(areaMapping : AreaMapping, 
                    stat : GameStat, 
                    datasetSplit : SeparatedData, 
                    summonerName : str,
                    time : int,
                    gameDuration : int):
    # areaMapping and stat objects must already be computed !
    # datasetSplit must be the right split of the game we want to analyse !
    

    participantID = datasetSplit.getPlayerID(summonerName)
    snapshot : Snapshot = datasetSplit.getSnapShotByTime(time, gameDuration)

    # Getting the team where the player is
    if datasetSplit.gameSnapshotList[0].teams[0].isPlayerInTeam(participantID):
        participantIdx : int = datasetSplit.gameSnapshotList[0].teams[0].getPlayerIdx(participantID)

        if roleMap[participantIdx] == "Top":
            (statDict, lanePresenceMapping) = getBehaviorDataTop(datasetSplit, snapshot, areaMapping, stat, participantIdx, summonerName, 0, gameDuration)
        elif roleMap[participantIdx] == "Jungle":
            (statDict, lanePresenceMapping) = getBehaviorDataJungle(datasetSplit, snapshot, areaMapping, stat, participantIdx, summonerName, 0, gameDuration)
        elif roleMap[participantIdx] == "Mid":
            (statDict, lanePresenceMapping) = getBehaviorDataMid(datasetSplit, snapshot, areaMapping, stat, participantIdx, summonerName, 0, gameDuration)
        elif roleMap[participantIdx] == "ADC":
            (statDict, lanePresenceMapping) = getBehaviorDataADC(datasetSplit, snapshot, areaMapping, stat, participantIdx, summonerName, 0, gameDuration)
        elif roleMap[participantIdx] == "Support":
            (statDict, lanePresenceMapping) = getBehaviorDataSupport(datasetSplit, snapshot, areaMapping, stat, participantIdx, summonerName, 0, gameDuration)
        
        return statDict, lanePresenceMapping

    elif datasetSplit.gameSnapshotList[0].teams[1].isPlayerInTeam(participantID):
        participantIdx : int = datasetSplit.gameSnapshotList[0].teams[1].getPlayerIdx(participantID)

        if roleMap[participantIdx] == "Top":
            (statDict, lanePresenceMapping) = getBehaviorDataTop(datasetSplit, snapshot, areaMapping, stat, participantIdx, summonerName, 1, gameDuration)
        elif roleMap[participantIdx] == "Jungle":
            (statDict, lanePresenceMapping) = getBehaviorDataJungle(datasetSplit, snapshot, areaMapping, stat, participantIdx, summonerName, 1, gameDuration)
        elif roleMap[participantIdx] == "Mid":
            (statDict, lanePresenceMapping) = getBehaviorDataMid(datasetSplit, snapshot, areaMapping, stat, participantIdx, summonerName, 1, gameDuration)
        elif roleMap[participantIdx] == "ADC":
            (statDict, lanePresenceMapping) = getBehaviorDataADC(datasetSplit, snapshot, areaMapping, stat, participantIdx, summonerName, 1, gameDuration)
        elif roleMap[participantIdx] == "Support":
            (statDict, lanePresenceMapping) = getBehaviorDataSupport(datasetSplit, snapshot, areaMapping, stat, participantIdx, summonerName, 1, gameDuration)
        
        return statDict, lanePresenceMapping

def getBehaviorDataTop(datasetSplit :SeparatedData,
                       snapshot : Snapshot, 
                       areaMapping : AreaMapping, 
                       stat : GameStat,
                       participantIdx : int,
                       summonerName : str,
                       team : int,
                       gameDuration : int):

    begGameTime = datasetSplit.begGameTime
    endGameTime = datasetSplit.endGameTime

    # Computing general statistics about the player
    statDict : dict = dict()
    
    if team == 0:
        statDict["XPD@15"] = stat.playerXPDiff[participantIdx]
        statDict["GD@15"] = stat.playerGoldDiff[participantIdx]
        statDict["CS/Min"] = 60*snapshot.teams[0].players[participantIdx].stats.minionsKilled/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Kills"] = snapshot.teams[0].players[participantIdx].stats.championsKilled
        statDict["Deaths"] = snapshot.teams[0].players[participantIdx].stats.numDeaths
        statDict["Assists"] = snapshot.teams[0].players[participantIdx].stats.assists

        if snapshot.teams[0].championKills > 0 :
            statDict["KP%"] = (statDict["Assists"] + statDict["Kills"])/snapshot.teams[0].championKills 
        else :
            statDict["KP%"] = 0

        statDict["WardPlaced"] = snapshot.teams[0].players[participantIdx].stats.wardPlaced

        statDict["Damage/Min"] = 60*snapshot.teams[0].players[participantIdx].stats.totalDamageDealtChampions/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["TotalDamageDealtToBuilding"] = snapshot.teams[0].players[participantIdx].stats.totalDamageDealtToBuildings
        statDict["TotalDamageDealtToObjectives"] = snapshot.teams[0].players[participantIdx].stats.totalDamageDealtToObjectives

        lanePresenceMapping : dict = dict()
        lanePresenceMapping["topLanePresence"] = areaMapping.teamOneMapping[summonerName]["topLanePresence"]
        lanePresenceMapping["jungleAllyTopPresence"] = areaMapping.teamOneMapping[summonerName]["jungleAllyTopPresence"]
        lanePresenceMapping["jungleEnemyTopPresence"] = areaMapping.teamOneMapping[summonerName]["jungleEnemyTopPresence"]
        lanePresenceMapping["riverTopPresence"] = areaMapping.teamOneMapping[summonerName]["riverTopPresence"]
        
        statDict["JungleProximity"] = getJungleProximity(datasetSplit, 0)[summonerName]
        
    
    if team == 1 : 
        statDict["XPD@15"] = -stat.playerXPDiff[participantIdx]
        statDict["GD@15"] = -stat.playerGoldDiff[participantIdx]
        statDict["CS/Min"] = 60*snapshot.teams[1].players[participantIdx].stats.minionsKilled/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Kills"] = snapshot.teams[1].players[participantIdx].stats.championsKilled
        statDict["Deaths"] = snapshot.teams[1].players[participantIdx].stats.numDeaths
        statDict["Assists"] = snapshot.teams[1].players[participantIdx].stats.assists
        if snapshot.teams[1].championKills > 0 :
            statDict["KP%"] = (statDict["Assists"] + statDict["Kills"])/snapshot.teams[1].championKills 
        else :
            statDict["KP%"] = 0

        statDict["WardPlaced"] = snapshot.teams[1].players[participantIdx].stats.wardPlaced

        statDict["Damage/Min"] = 60*snapshot.teams[1].players[participantIdx].stats.totalDamageDealtChampions/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["TotalDamageDealtToBuilding"] = snapshot.teams[1].players[participantIdx].stats.totalDamageDealtToBuildings
        statDict["TotalDamageDealtToObjectives"] = snapshot.teams[1].players[participantIdx].stats.totalDamageDealtToObjectives

        lanePresenceMapping : dict = dict()
        lanePresenceMapping["topLanePresence"] = areaMapping.teamTwoMapping[summonerName]["topLanePresence"]
        lanePresenceMapping["jungleAllyTopPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleAllyTopPresence"]
        lanePresenceMapping["jungleEnemyTopPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleEnemyTopPresence"]
        lanePresenceMapping["riverTopPresence"] = areaMapping.teamTwoMapping[summonerName]["riverTopPresence"]
        
        statDict["JungleProximity"] = getJungleProximity(datasetSplit, 1)[summonerName]
    return statDict, lanePresenceMapping
def getBehaviorDataJungle(datasetSplit :SeparatedData,
                       snapshot : Snapshot, 
                       areaMapping : AreaMapping, 
                       stat : GameStat,
                       participantIdx : int,
                       summonerName : str,
                       team : int,
                       gameDuration : int):
    
    begGameTime = datasetSplit.begGameTime
    endGameTime = datasetSplit.endGameTime

    # Computing general statistics about the player
    statDict : dict = dict()
    if team == 0:
        statDict["XPD@15"] = stat.playerXPDiff[participantIdx]
        statDict["GD@15"] = stat.playerGoldDiff[participantIdx]
        statDict["Kills"] = snapshot.teams[0].players[participantIdx].stats.championsKilled
        statDict["Deaths"] = snapshot.teams[0].players[participantIdx].stats.numDeaths
        statDict["Assists"] = snapshot.teams[0].players[participantIdx].stats.assists
        if snapshot.teams[0].championKills > 0 :
            statDict["KP%"] = (statDict["Assists"] + statDict["Kills"])/snapshot.teams[0].championKills 
        else :
            statDict["KP%"] = 0


        statDict["Damage/Min"] = 60*snapshot.teams[0].players[participantIdx].stats.totalDamageDealtChampions/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)

        lanePresenceMapping : dict = dict()
        lanePresenceMapping["topLanePresence"] = areaMapping.teamOneMapping[summonerName]["topLanePresence"]
        lanePresenceMapping["midLanePresence"] = areaMapping.teamOneMapping[summonerName]["midLanePresence"]
        lanePresenceMapping["botLanePresence"] = areaMapping.teamOneMapping[summonerName]["botLanePresence"]
                
        lanePresenceMapping["jungleAllyTopPresence"] = areaMapping.teamOneMapping[summonerName]["jungleAllyTopPresence"]
        lanePresenceMapping["jungleAllyBotPresence"] = areaMapping.teamOneMapping[summonerName]["jungleAllyBotPresence"]
        lanePresenceMapping["jungleEnemyTopPresence"] = areaMapping.teamOneMapping[summonerName]["jungleEnemyTopPresence"]
        lanePresenceMapping["jungleEnemyBotPresence"] = areaMapping.teamOneMapping[summonerName]["jungleEnemyBotPresence"]

        lanePresenceMapping["riverBotPresence"] = areaMapping.teamOneMapping[summonerName]["riverBotPresence"]
        lanePresenceMapping["riverTopPresence"] = areaMapping.teamOneMapping[summonerName]["riverTopPresence"]

    if team == 1 :
        statDict["XPD@15"] = - stat.playerXPDiff[participantIdx]
        statDict["GD@15"] = - stat.playerGoldDiff[participantIdx]
        statDict["Kills"] = snapshot.teams[1].players[participantIdx].stats.championsKilled
        statDict["Deaths"] = snapshot.teams[1].players[participantIdx].stats.numDeaths
        statDict["Assists"] = snapshot.teams[1].players[participantIdx].stats.assists
        if snapshot.teams[1].championKills > 0 :
            statDict["KP%"] = (statDict["Assists"] + statDict["Kills"])/snapshot.teams[1].championKills 
        else :
            statDict["KP%"] = 0

        statDict["Damage/Min"] = 60*snapshot.teams[1].players[participantIdx].stats.totalDamageDealtChampions/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)

    
        lanePresenceMapping : dict = dict()
        lanePresenceMapping["topLanePresence"] = areaMapping.teamTwoMapping[summonerName]["topLanePresence"]
        lanePresenceMapping["midLanePresence"] = areaMapping.teamTwoMapping[summonerName]["midLanePresence"]
        lanePresenceMapping["botLanePresence"] = areaMapping.teamTwoMapping[summonerName]["botLanePresence"]
        
        lanePresenceMapping["jungleAllyTopPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleAllyTopPresence"]
        lanePresenceMapping["jungleAllyBotPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleAllyBotPresence"]
        lanePresenceMapping["jungleEnemyTopPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleEnemyTopPresence"]
        lanePresenceMapping["jungleEnemyBotPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleEnemyBotPresence"]

        lanePresenceMapping["riverBotPresence"] = areaMapping.teamTwoMapping[summonerName]["riverBotPresence"]
        lanePresenceMapping["riverTopPresence"] = areaMapping.teamTwoMapping[summonerName]["riverTopPresence"]
    
    return statDict, lanePresenceMapping
def getBehaviorDataMid(datasetSplit :SeparatedData,
                       snapshot : Snapshot, 
                       areaMapping : AreaMapping, 
                       stat : GameStat,
                       participantIdx : int,
                       summonerName : str,
                       team : int,
                       gameDuration : int):
    
    begGameTime = datasetSplit.begGameTime
    endGameTime = datasetSplit.endGameTime

    # Computing general statistics about the player
    statDict : dict = dict()
    if team == 0:
        statDict["XPD@15"] = stat.playerXPDiff[participantIdx]
        statDict["GD@15"] = stat.playerGoldDiff[participantIdx]
        statDict["CS/Min"] = 60*snapshot.teams[0].players[participantIdx].stats.minionsKilled/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Kills"] = snapshot.teams[0].players[participantIdx].stats.championsKilled
        statDict["Deaths"] = snapshot.teams[0].players[participantIdx].stats.numDeaths
        statDict["Assists"] = snapshot.teams[0].players[participantIdx].stats.assists
        if snapshot.teams[0].championKills > 0 :
            statDict["KP%"] = (statDict["Assists"] + statDict["Kills"])/snapshot.teams[0].championKills 
        else :
            statDict["KP%"] = 0

        statDict["WardPlaced"] = snapshot.teams[0].players[participantIdx].stats.wardPlaced
        statDict["WardKilled"] = snapshot.teams[0].players[participantIdx].stats.wardKilled

        statDict["Damage/Min"] = 60*snapshot.teams[0].players[participantIdx].stats.totalDamageDealtChampions/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["TotalDamageDealtToBuilding"] = snapshot.teams[0].players[participantIdx].stats.totalDamageDealtToBuildings
        statDict["TotalDamageDealtToObjectives"] = snapshot.teams[0].players[participantIdx].stats.totalDamageDealtToObjectives

        lanePresenceMapping : dict = dict()
        lanePresenceMapping["topLanePresence"] = areaMapping.teamOneMapping[summonerName]["topLanePresence"]
        lanePresenceMapping["midLanePresence"] = areaMapping.teamOneMapping[summonerName]["midLanePresence"]
        lanePresenceMapping["botLanePresence"] = areaMapping.teamOneMapping[summonerName]["botLanePresence"]
        
        lanePresenceMapping["jungleAllyTopPresence"] = areaMapping.teamOneMapping[summonerName]["jungleAllyTopPresence"]
        lanePresenceMapping["jungleAllyBotPresence"] = areaMapping.teamOneMapping[summonerName]["jungleAllyBotPresence"]

        lanePresenceMapping["jungleEnemyTopPresence"] = areaMapping.teamOneMapping[summonerName]["jungleEnemyTopPresence"]
        lanePresenceMapping["jungleEnemyBotPresence"] = areaMapping.teamOneMapping[summonerName]["jungleEnemyBotPresence"]
        
        lanePresenceMapping["riverBotPresence"] = areaMapping.teamOneMapping[summonerName]["riverBotPresence"]
        lanePresenceMapping["riverTopPresence"] = areaMapping.teamOneMapping[summonerName]["riverTopPresence"]

        statDict["JungleProximity"] = getJungleProximity(datasetSplit, 0)[summonerName]
    if team == 1 :
        statDict["XPD@15"] = - stat.playerXPDiff[participantIdx]
        statDict["GD@15"] = - stat.playerGoldDiff[participantIdx]
        statDict["CS/Min"] = 60*snapshot.teams[1].players[participantIdx].stats.minionsKilled/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Kills"] = snapshot.teams[1].players[participantIdx].stats.championsKilled
        statDict["Deaths"] = snapshot.teams[1].players[participantIdx].stats.numDeaths
        statDict["Assists"] = snapshot.teams[1].players[participantIdx].stats.assists
        
        if snapshot.teams[1].championKills > 0 :
            statDict["KP%"] = (statDict["Assists"] + statDict["Kills"])/snapshot.teams[1].championKills 
        else :
            statDict["KP%"] = 0

        statDict["WardPlaced"] = snapshot.teams[1].players[participantIdx].stats.wardPlaced
        statDict["WardKilled"] = snapshot.teams[1].players[participantIdx].stats.wardKilled

        statDict["Damage/Min"] = 60*snapshot.teams[1].players[participantIdx].stats.totalDamageDealtChampions/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["TotalDamageDealtToBuilding"] = snapshot.teams[1].players[participantIdx].stats.totalDamageDealtToBuildings
        statDict["TotalDamageDealtToObjectives"] = snapshot.teams[1].players[participantIdx].stats.totalDamageDealtToObjectives

        lanePresenceMapping : dict = dict()
        lanePresenceMapping["topLanePresence"] = areaMapping.teamTwoMapping[summonerName]["topLanePresence"]
        lanePresenceMapping["midLanePresence"] = areaMapping.teamTwoMapping[summonerName]["midLanePresence"]
        lanePresenceMapping["botLanePresence"] = areaMapping.teamTwoMapping[summonerName]["botLanePresence"]

        lanePresenceMapping["jungleAllyTopPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleAllyTopPresence"]
        lanePresenceMapping["jungleAllyBotPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleAllyBotPresence"]

        lanePresenceMapping["jungleEnemyTopPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleEnemyTopPresence"]
        lanePresenceMapping["jungleEnemyBotPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleEnemyBotPresence"]
        
        lanePresenceMapping["riverBotPresence"] = areaMapping.teamTwoMapping[summonerName]["riverBotPresence"]
        lanePresenceMapping["riverTopPresence"] = areaMapping.teamTwoMapping[summonerName]["riverTopPresence"]
        
        statDict["JungleProximity"] = getJungleProximity(datasetSplit, 1)[summonerName]
    
    
    return statDict, lanePresenceMapping
def getBehaviorDataADC(datasetSplit :SeparatedData,
                       snapshot : Snapshot, 
                       areaMapping : AreaMapping, 
                       stat : GameStat,
                       participantIdx : int,
                       summonerName : str,
                       team : int,
                       gameDuration : int):
    begGameTime = datasetSplit.begGameTime
    endGameTime = datasetSplit.endGameTime

    # Computing general statistics about the player
    statDict : dict = dict()

    if team == 0:
        statDict["XPD@15"] = stat.playerXPDiff[participantIdx]
        statDict["GD@15"] = stat.playerGoldDiff[participantIdx]
        statDict["CS/Min"] = 60*snapshot.teams[0].players[participantIdx].stats.minionsKilled/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Kills"] = snapshot.teams[0].players[participantIdx].stats.championsKilled
        statDict["Deaths"] = snapshot.teams[0].players[participantIdx].stats.numDeaths
        statDict["Assists"] = snapshot.teams[0].players[participantIdx].stats.assists
        if snapshot.teams[0].championKills > 0 :
            statDict["KP%"] = (statDict["Assists"] + statDict["Kills"])/snapshot.teams[0].championKills 
        else :
            statDict["KP%"] = 0


        statDict["Damage/Min"] = 60*snapshot.teams[0].players[participantIdx].stats.totalDamageDealtChampions/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)

        lanePresenceMapping : dict = dict()
        lanePresenceMapping["botLanePresence"] = areaMapping.teamOneMapping[summonerName]["botLanePresence"]
        
        lanePresenceMapping["riverBotPresence"] =  areaMapping.teamOneMapping[summonerName]["riverBotPresence"]
        
        statDict["JungleProximity"] = getJungleProximity(datasetSplit, 0)[summonerName]
    if team == 1 :
        statDict["XPD@15"] = - stat.playerXPDiff[participantIdx]
        statDict["GD@15"] = - stat.playerGoldDiff[participantIdx] 
        statDict["CS/Min"] = 60*snapshot.teams[1].players[participantIdx].stats.minionsKilled/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)
        statDict["Kills"] = snapshot.teams[1].players[participantIdx].stats.championsKilled
        statDict["Deaths"] = snapshot.teams[1].players[participantIdx].stats.numDeaths
        statDict["Assists"] = snapshot.teams[1].players[participantIdx].stats.assists
        
        if snapshot.teams[1].championKills > 0 :
            statDict["KP%"] = (statDict["Assists"] + statDict["Kills"])/snapshot.teams[1].championKills 
        else :
            statDict["KP%"] = 0


        statDict["Damage/Min"] = 60*snapshot.teams[1].players[participantIdx].stats.totalDamageDealtChampions/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)

        lanePresenceMapping : dict = dict()
        lanePresenceMapping["botLanePresence"] = areaMapping.teamTwoMapping[summonerName]["botLanePresence"]
        
        lanePresenceMapping["riverBotPresence"] =  areaMapping.teamTwoMapping[summonerName]["riverBotPresence"]
        
        statDict["JungleProximity"] = getJungleProximity(datasetSplit, 1)[summonerName]
    
    return statDict, lanePresenceMapping
def getBehaviorDataSupport(datasetSplit :SeparatedData,
                       snapshot : Snapshot, 
                       areaMapping : AreaMapping, 
                       stat : GameStat,
                       participantIdx : int,
                       summonerName : str,
                       team : int,
                       gameDuration : int):
    
    begGameTime = datasetSplit.begGameTime
    endGameTime = datasetSplit.endGameTime

    # Computing general statistics about the player
    statDict : dict = dict()
    if team == 0:
        statDict["XPD@15"] = - stat.playerXPDiff[participantIdx]
        statDict["GD@15"] = - stat.playerGoldDiff[participantIdx]
        statDict["Deaths"] = snapshot.teams[0].players[participantIdx].stats.numDeaths

        if snapshot.teams[0].championKills > 0 :
            statDict["KP%"] = (snapshot.teams[0].players[participantIdx].stats.assists + snapshot.teams[0].players[participantIdx].stats.championsKilled)/snapshot.teams[0].championKills
        else :
            statDict["KP%"] = 0

        statDict["WardPlaced"] = snapshot.teams[0].players[participantIdx].stats.wardPlaced
        statDict["WardKilled"] = snapshot.teams[0].players[participantIdx].stats.wardKilled

        statDict["Damage/Min"] = 60*snapshot.teams[0].players[participantIdx].stats.totalDamageDealtChampions/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)

        lanePresenceMapping : dict = dict()
        lanePresenceMapping["topLanePresence"] = areaMapping.teamOneMapping[summonerName]["topLanePresence"]
        lanePresenceMapping["midLanePresence"] = areaMapping.teamOneMapping[summonerName]["midLanePresence"]
        lanePresenceMapping["botLanePresence"] = areaMapping.teamOneMapping[summonerName]["botLanePresence"]
        
        lanePresenceMapping["jungleAllyTopPresence"] = areaMapping.teamOneMapping[summonerName]["jungleAllyTopPresence"]
        lanePresenceMapping["jungleAllyBotPresence"] = areaMapping.teamOneMapping[summonerName]["jungleAllyBotPresence"]
        lanePresenceMapping["jungleEnemyTopPresence"] = areaMapping.teamOneMapping[summonerName]["jungleEnemyTopPresence"]
        lanePresenceMapping["jungleEnemyBotPresence"] = areaMapping.teamOneMapping[summonerName]["jungleEnemyBotPresence"]

        lanePresenceMapping["riverBotPresence"] = areaMapping.teamOneMapping[summonerName]["riverBotPresence"]
        lanePresenceMapping["riverTopPresence"] = areaMapping.teamOneMapping[summonerName]["riverTopPresence"]

        statDict["JungleProximity"] = getJungleProximity(datasetSplit, 0)[summonerName]
    if team == 1 :
        statDict["XPD@15"] = - stat.playerXPDiff[participantIdx]
        statDict["GD@15"] = - stat.playerGoldDiff[participantIdx]
        statDict["Deaths"] = snapshot.teams[1].players[participantIdx].stats.numDeaths
        
        if snapshot.teams[1].championKills > 0 :
            statDict["KP%"] = (snapshot.teams[1].players[participantIdx].stats.assists + snapshot.teams[1].players[participantIdx].stats.championsKilled)/snapshot.teams[1].championKills
        else :
            statDict["KP%"] = 0
        
        statDict["WardPlaced"] = snapshot.teams[1].players[participantIdx].stats.wardPlaced
        statDict["WardKilled"] = snapshot.teams[1].players[participantIdx].stats.wardKilled

        statDict["Damage/Min"] = 60*snapshot.teams[1].players[participantIdx].stats.totalDamageDealtChampions/snapshot.convertGameTimeToSeconds(gameDuration, begGameTime,endGameTime)

        lanePresenceMapping : dict = dict()
        lanePresenceMapping["topLanePresence"] = areaMapping.teamTwoMapping[summonerName]["topLanePresence"]
        lanePresenceMapping["midLanePresence"] = areaMapping.teamTwoMapping[summonerName]["midLanePresence"]
        lanePresenceMapping["botLanePresence"] = areaMapping.teamTwoMapping[summonerName]["botLanePresence"]
        
        lanePresenceMapping["jungleAllyTopPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleAllyTopPresence"]
        lanePresenceMapping["jungleAllyBotPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleAllyBotPresence"]
        lanePresenceMapping["jungleEnemyTopPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleEnemyTopPresence"]
        lanePresenceMapping["jungleEnemyBotPresence"] = areaMapping.teamTwoMapping[summonerName]["jungleEnemyBotPresence"]

        lanePresenceMapping["riverBotPresence"] = areaMapping.teamTwoMapping[summonerName]["riverBotPresence"]
        lanePresenceMapping["riverTopPresence"] = areaMapping.teamTwoMapping[summonerName]["riverTopPresence"]
    
        
        statDict["JungleProximity"] = getJungleProximity(datasetSplit, 1)[summonerName]
    
    
    return statDict, lanePresenceMapping

# TODO: MODIFY FOLLOWING FUNCTION
def saveToDataBase(statDict : dict, 
                   lanePresenceMapping : dict,
                   path : str,
                   new : bool,
                   matchId : str,
                   seriesId : str,
                   patch : str,
                   summonnerName : str,
                   role : str,
                   tournament : str,
                   date : str,
                   gameNumber : int):
    
    # Asserting the right open option

    if new:
        open_option = 'w'
    else:
        open_option = 'a'
    
    full_path = path + "behavior_{}.csv".format(role)


    with open(full_path, open_option) as csv_file:
        
        writer = csv.writer(csv_file, delimiter=";")
        if new :
            header = ["Date", "Tournament", "MatchId", "SeriesId", "Patch", "SummonnerName"]
            for key in statDict.keys():
                header.append(key)
            for key in lanePresenceMapping.keys():
                header.append(key)
            
            header.append("GameNumber")
            writer.writerow(header)
        
        elif not(isInDataBase(matchId, date, role, summonnerName)):
            data : list = list()
            data.append(date)
            data.append(tournament)
            data.append(matchId)
            data.append(seriesId)
            data.append(patch)
            data.append(summonnerName)
            for _, v in statDict.items():
                data.append(v)
            for _, v in lanePresenceMapping.items():
                data.append(v)
            data.append(gameNumber)
            writer.writerow(data)