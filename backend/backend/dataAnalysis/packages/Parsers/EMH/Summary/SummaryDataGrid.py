import json
import pandas as pd

from dataAnalysis.packages.Parsers.EMH.Summary.TeamEndGameStatGrid import TeamEndGameStatGrid
from dataAnalysis.packages.Parsers.EMH.Summary.ObjectiveGrid import ObjectiveGrid
from dataAnalysis.packages.Parsers.EMH.Summary.PlayerEndGameStatGrid import PlayerEndGameStatGrid
from dataAnalysis.packages.Parsers.EMH.Summary.AssistObject import AssistObject

class SummaryDataGrid:
    def __init__(self, json_path : str):
        self.json_path = json_path
        
        with open(json_path) as f:
            data = json.loads(f.read())
        
        print(json.dumps(data, indent=4))
        
        # Parsing global info
        self.seriesType = data["format"]
        
        # Parsing global team info
        self.teams : list[TeamEndGameStatGrid] = list()
        for teamDict in data["teams"]:
            
            # parsing objectives
            objectives : list[ObjectiveGrid] = list()
            for objectiveDict in teamDict["objectives"]:
                objectives.append(
                    ObjectiveGrid(
                        objectiveDict["id"],
                        objectiveDict["type"],
                        objectiveDict["completionCount"]
                    )
                )
            
            # parsing players
            players : list[PlayerEndGameStatGrid] = list()
            for playerDict in teamDict["players"]:
                playerId : str = playerDict["id"]
                killAssistsReceivedFromPlayer : list[AssistObject] = list()
                for assistDict in playerDict["killAssistsReceivedFromPlayer"]:
                    killAssistsReceivedFromPlayer.append(
                        AssistObject(
                            playerId,
                            assistDict["playerId"],
                            assistDict["killAssistsReceived"]
                        )
                    )
                    
                objectives : list[ObjectiveGrid] = list()
                for objectiveDict in playerDict["objectives"]:
                    objectives.append(ObjectiveGrid(
                        objectiveDict["id"],
                        objectiveDict["type"],
                        objectiveDict["completionCount"]
                    ))
                
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
                        objectives
                    )
                )
            
            self.teams.append(
                TeamEndGameStatGrid(
                    teamDict["id"],
                    teamDict["name"],
                    teamDict["score"],
                    teamDict["won"],
                    teamDict["kills"],
                    teamDict["killAssistsReceived"],
                    teamDict["killAssistsGiven"],
                    teamDict["deaths"],
                    teamDict["structuresDestroyed"],
                    objectives,
                    players
                )
            )
    
    def getObjectiveCount(self, side : int, objectiveId : str) -> int:
        # Blue side : 0, red side : 1
        objectiveObject : ObjectiveGrid
        for objectiveObject in self.teams[side].objectives:
            if objectiveObject.id == objectiveId:
                return objectiveObject.completionCount
            
    def getDrakeCount(self, side : int) -> int:
        # Blue side : 0, red side : 1
        objectiveObject : ObjectiveGrid
        completionCount : int = 0
        for objectiveObject in self.teams[side].objectives:
            if "Drake" in objectiveObject.id:
                completionCount += objectiveObject.completionCount
        return completionCount
    
    def getGrubsCount(self, side : int) -> int:
        # Blue side : 0, red side : 1
        objectiveObject : ObjectiveGrid
        for objectiveObject in self.teams[side].objectives:
            if objectiveObject.id == "slayVoidGrub":
                return objectiveObject.completionCount