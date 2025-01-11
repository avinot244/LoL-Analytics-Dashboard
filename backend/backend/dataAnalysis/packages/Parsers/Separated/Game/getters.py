from tqdm import tqdm
import re

from dataAnalysis.packages.Parsers.Separated.Game.SeparatedData import SeparatedData
from dataAnalysis.packages.Parsers.Separated.Game.Snapshot import Snapshot
from dataAnalysis.packages.utils_stuff.reset_trigger import didPlayerReset
from dataAnalysis.packages.Parsers.Separated.Events.EventTypes import *

def getResetTriggers(data : SeparatedData , gameDuration : int):
    result : dict = {
        "blueTeam": {},
        "redTeam": {}
    }
    
    firstSnapshot : Snapshot = data.gameSnapshotList[0]
    for player in firstSnapshot.teams[0].players:
        result["blueTeam"][player.playerName] = []
        
    for player in firstSnapshot.teams[1].players:
        result["redTeam"][player.playerName] = []
    
    for time in tqdm(range(gameDuration + 1)):
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

def getWardTriggers(data : SeparatedData):
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
        if event_name == "ward_placed":
            event : WardPlacedEvent
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
                "time": event.gameTime,
                "position": event.position,
                "wardType": event.wardType
            })
            
    return result