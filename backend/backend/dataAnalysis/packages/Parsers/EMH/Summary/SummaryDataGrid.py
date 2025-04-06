import json
import pandas as pd

from dataAnalysis.packages.Parsers.EMH.Summary.TeamEndGameStatGrid import TeamEndGameStatGrid
from dataAnalysis.packages.Parsers.EMH.Summary.ObjectiveGrid import ObjectiveGrid
from dataAnalysis.packages.Parsers.EMH.Summary.PlayerEndGameStatGrid import PlayerEndGameStatGrid
from dataAnalysis.packages.Parsers.EMH.Summary.AssistObject import AssistObject

class SummaryDataGrid:
    def __init__(self, json_path : str, gameNumber : int):
        self.json_path = json_path
        self.gameNumber = gameNumber-1
        
        with open(json_path) as f:
            data = json.loads(f.read())
        
        # Parsing global info
        if list(data.keys())[0] == "seriesState" and len(list(data.keys())) == 1:
            data = data["seriesState"]
        self.seriesType = data["format"]
        
        # Parsing global team info
        self.teams : list[TeamEndGameStatGrid] = []
        for teamDict in data["games"][self.gameNumber]["teams"]:
            # parsing objectives
            objectives : list[ObjectiveGrid] = []
            for objectiveDict in teamDict["objectives"]:
                objectives.append(
                    ObjectiveGrid(
                        objectiveDict["id"],
                        objectiveDict["type"],
                        objectiveDict["completionCount"]
                    )
                )
            # parsing players
            players : list[PlayerEndGameStatGrid] = []
            for playerDict in teamDict["players"]:
                playerId : str = playerDict["id"]
                killAssistsReceivedFromPlayer : list[AssistObject] = []
                for assistDict in playerDict["killAssistsReceivedFromPlayer"]:
                    killAssistsReceivedFromPlayer.append(
                        AssistObject(
                            playerId,
                            assistDict["playerId"],
                            assistDict["killAssistsReceived"]
                        )
                    )
                
                players.append(
                    PlayerEndGameStatGrid(
                        playerDict["id"],
                        playerDict["name"],
                        playerDict["kills"],
                        playerDict["killAssistsReceived"],
                        playerDict["killAssistsGiven"],
                        killAssistsReceivedFromPlayer,
                        playerDict["deaths"],
                        playerDict["structuresDestroyed"],
                    )
                )
            
            self.teams.append(
                TeamEndGameStatGrid(
                    teamDict["id"],
                    teamDict["name"],
                    teamDict["score"],
                    teamDict["kills"],
                    teamDict["killAssistsReceived"],
                    teamDict["killAssistsGiven"],
                    teamDict["deaths"],
                    teamDict["structuresDestroyed"],
                    objectives,
                    players
                )
            )
    
    def getDrakeCount(self, side : int) -> int:
        # Blue side : 0, red side : 1
        objectiveObject : ObjectiveGrid
        completionCount : int = 0
        if len(self.teams[side].objectives) == 0:
            return 0
        else:
            for objectiveObject in self.teams[side].objectives:
                if "Drake" in objectiveObject.id:
                    completionCount += objectiveObject.completionCount
            return completionCount
    
    def getGrubsCount(self, side : int) -> int:
        # Blue side : 0, red side : 1
        objectiveObject : ObjectiveGrid
        if len(self.teams[side].objectives) == 0:
            return 0
        else:
            for objectiveObject in self.teams[side].objectives:
                if objectiveObject.id == "slayVoidGrub":
                    return objectiveObject.completionCount
            return 0