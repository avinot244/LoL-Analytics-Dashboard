from tqdm import tqdm
import re
import json

from dataAnalysis.packages.utils_stuff.utils_func import convertTime
from dataAnalysis.packages.utils_stuff.Position import Position
from dataAnalysis.packages.Parsers.Separated.Game.SeparatedData import SeparatedData
from dataAnalysis.packages.Parsers.Separated.Game.Snapshot import Snapshot
from dataAnalysis.packages.utils_stuff.triggers import didPlayerReset
from dataAnalysis.packages.Parsers.Separated.Events.EventTypes import *

def getKillTriggers(data : SeparatedData, gameDuration : int, endGameTime : int, begTime : int, endTime : int):
    result : dict = {
        "blueTeam": [],
        "redTeam": []
    }
    for event in data.eventList:
        event_name : str = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', event.__class__.__name__.replace("Event", "")).lower()
        if event_name == "champion_kill":
            event : ChampionKillEvent
            time = convertTime(event.gameTime, gameDuration, endGameTime)
            if time <= endTime and time >= begTime:
                if event.killerTeamID == 100:
                    result["blueTeam"].append({
                        "time": time,
                        "position": event.position
                    })
                else: 
                    result["redTeam"].append({
                        "time": time,
                        "position": event.position
                    })
    return result

def getPlayerPositionHistoryTimeFramed(data : SeparatedData , gameDuration: int, participantID : int, begTime : int, endTime : int) -> list[Position]:
    positionList : list[Position] = list()
    
    splitList : list[int] = [begTime, endTime]    
    data : SeparatedData = data.splitData(gameDuration, splitList)[1]
    
    for gameSnapshot in data.gameSnapshotList:
        if gameSnapshot.teams[0].isPlayerInTeam(participantID):
            playerIdx : int = gameSnapshot.teams[0].getPlayerIdx(participantID)
            if gameSnapshot.teams[0].players[playerIdx].isAlive():
                positionPlayer : Position = gameSnapshot.teams[0].getPlayerPosition(playerIdx)
                positionList.append(positionPlayer)
        else:
            playerIdx : int = gameSnapshot.teams[1].getPlayerIdx(participantID)
            if gameSnapshot.teams[1].players[playerIdx].isAlive():
                positionPlayer : Position = gameSnapshot.teams[1].getPlayerPosition(playerIdx)
                positionList.append(positionPlayer)
    return positionList

def getResetTriggers(data : SeparatedData , gameDuration : int, begTime : int, endTime : int, verbose : bool = True):
    result : dict = {
        "blueTeam": {},
        "redTeam": {}
    }
    
    firstSnapshot : Snapshot = data.gameSnapshotList[0]
    for player in firstSnapshot.teams[0].players:
        result["blueTeam"][player.playerName] = []
        
    for player in firstSnapshot.teams[1].players:
        result["redTeam"][player.playerName] = []
    
    for time in tqdm(range(begTime, endTime + 1), disable=not(verbose)):
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
    
    return result

def getTPTriggers(data : SeparatedData, gameDuration : int, endGameTime : int, begTime : int, endTime : int):
    result : dict = {
        "blueTeam": {},
        "redTeam": {}
    }
    firstSnapshot : Snapshot = data.gameSnapshotList[0]
    for player in firstSnapshot.teams[0].players:
        result["blueTeam"][player.playerName] = []
        
    for player in firstSnapshot.teams[1].players:
        result["redTeam"][player.playerName] = []
    
    for event in data.eventList:
        if isinstance(event, ChannelingEndedEvent):
            time = convertTime(event.gameTime, gameDuration, endGameTime)
            if time <= endTime and time >= begTime and event.channelingType == "summonerSpell":
                participantID : int = event.participantID
                
                # Get the player name and team info
                team : str = ""
                teamIdx : int = 0
                playerName : str = ""
                if data.gameSnapshotList[0].teams[0].isPlayerInTeam(participantID):
                    team = "blueTeam"
                    teamIdx = 0
                    playerName = data.gameSnapshotList[0].teams[0].getPlayerNameFromID(participantID)
                elif data.gameSnapshotList[0].teams[1].isPlayerInTeam(participantID):
                    team = "redTeam"
                    teamIdx = 1
                    playerName = data.gameSnapshotList[0].teams[1].getPlayerNameFromID(participantID)
                    
                gameSnapshot : Snapshot = data.getSnapShotByTime(time + 1, gameDuration) # Adding a small time offset to guaratee that we wait until the end of the TP to get his position
                
                # Get the TP target position
                playerIdx : int = gameSnapshot.teams[teamIdx].getPlayerIdx(participantID)
                position = gameSnapshot.teams[teamIdx].players[playerIdx].position.__dict__
                
                
                result[team][playerName].append({
                    "time": time,
                    "position": position
                })
    return result
        

def getWardTriggers(data : SeparatedData, gameDuration : int, endGameTime : int, begTime : int, endTime : int):
    result : dict = {
        "blueTeam": {},
        "redTeam": {}
    }
        
    firstSnapshot : Snapshot = data.gameSnapshotList[0]
    for player in firstSnapshot.teams[0].players:
        result["blueTeam"][player.playerName] = []
        
    for player in firstSnapshot.teams[1].players:
        result["redTeam"][player.playerName] = []
    
    for event in data.eventList:
        event_name : str = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', event.__class__.__name__.replace("Event", "")).lower()
        
        if event_name == "ward_placed": # also check if the event time is within begTime and endTime
            event : WardPlacedEvent
            time = convertTime(event.gameTime, gameDuration, endGameTime)
            if time <= endTime and time >= begTime and event.wardType != "unknown":
                participantID : int = event.placer
                
                team : str = ""
                playerName : str = ""
                if data.gameSnapshotList[0].teams[0].isPlayerInTeam(participantID):
                    team = "blueTeam"
                    playerName = data.gameSnapshotList[0].teams[0].getPlayerNameFromID(participantID)
                elif data.gameSnapshotList[0].teams[1].isPlayerInTeam(participantID):
                    team = "redTeam"
                    playerName = data.gameSnapshotList[0].teams[1].getPlayerNameFromID(participantID)
                
                result[team][playerName].append({
                    "time": time,
                    "position": event.position,
                    "wardType": event.wardType
                })
            
    return result