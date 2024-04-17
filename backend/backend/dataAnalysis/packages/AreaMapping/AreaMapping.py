from dataAnalysis.packages.Parsers.Separated.Game.SeparatedData import SeparatedData
from .Grid import Grid
from .Zone import Zone

from dataAnalysis.packages.utils_stuff.globals import *


class AreaMapping:
    def __init__(self) -> None:
        self.midLanePresenceGrid : Grid = Grid([Zone(midLaneBoundary)])
        self.topLanePresenceGrid : Grid = Grid([Zone(topLaneBoundary)])
        self.botLanePresenceGrid : Grid = Grid([Zone(botLaneBoundary)])

        self.jungleBlueTopPresenceGrid : Grid = Grid([Zone(jungleBlueBot),
                                                      Zone(jungleEntry1Blue),
                                                      Zone(jungleEntry2Blue)])
        
        self.jungleRedTopPresenceGrid : Grid = Grid([Zone(jungleRedTop),
                                                     Zone(jungleEntry1Red),
                                                     Zone(jungleEntry2Red)])
        
        self.jungleBlueBotPresenceGrid : Grid = Grid([Zone(jungleBlueBot),
                                                      Zone(jungleEntry3Blue),
                                                      Zone(jungleEntry4Blue)])
        
        self.jungleRedBotPresenceGrid : Grid = Grid([Zone(jungleRedBot),
                                                     Zone(jungleEntry3Red),
                                                     Zone(jungleEntry4Red)])
        
        
        self.riverBotPresenceGrid : Grid = Grid([Zone(riverBot)])
        self.riverTopPresenceGrid : Grid = Grid([Zone(riverTop)])
        
        self.forwardMidBlue : list[Grid] = None
        self.forwardMidRed : list[Grid] = None
        # For forward % we can do a list of grid for each lane where in each grid we have the forward degree zone
        
        self.teamOneMapping : dict = dict()
        self.teamTwoMapping : dict = dict()
    
    def computeMapping(self, data : SeparatedData):
        playerList = [data.gameSnapshotList[0].teams[0].getPlayerList(), data.gameSnapshotList[0].teams[1].getPlayerList()]
        
        for summonerName in playerList[0]:
            self.teamOneMapping[summonerName] = {"midLanePresence":0, 
                                                "topLanePresence":0, 
                                                "botLanePresence":0,
                                                "jungleAllyTopPresence":0,
                                                "jungleAllyBotPresence":0,
                                                "jungleEnemyTopPresence":0,
                                                "jungleEnemyBotPresence":0,
                                                "riverBotPresence":0,
                                                "riverTopPresence":0}
        for summonerName in playerList[1]:
            self.teamTwoMapping[summonerName] = {"midLanePresence":0, 
                                                "topLanePresence":0, 
                                                "botLanePresence":0,
                                                "riverBotPresence":0,
                                                "riverTopPresence":0,
                                                "jungleAllyTopPresence":0,
                                                "jungleAllyBotPresence":0,
                                                "jungleEnemyTopPresence":0,
                                                "jungleEnemyBotPresence":0}
        l = len(data.gameSnapshotList)
        for snapshot in data.gameSnapshotList:
            # For team one
            for player in snapshot.teams[0].players:
                if self.midLanePresenceGrid.containsPoint(player.position):
                    self.teamOneMapping[player.playerName]['midLanePresence'] += 1
                if self.topLanePresenceGrid.containsPoint(player.position):
                    self.teamOneMapping[player.playerName]['topLanePresence'] += 1
                if self.botLanePresenceGrid.containsPoint(player.position):
                    self.teamOneMapping[player.playerName]['botLanePresence'] += 1
                
                if self.riverBotPresenceGrid.containsPoint(player.position):
                    self.teamOneMapping[player.playerName]['riverBotPresence'] += 1
                if self.riverTopPresenceGrid.containsPoint(player.position):
                    self.teamOneMapping[player.playerName]['riverTopPresence'] += 1

                if self.jungleBlueTopPresenceGrid.containsPoint(player.position):
                    self.teamOneMapping[player.playerName]['jungleAllyTopPresence'] += 1
                if self.jungleBlueBotPresenceGrid.containsPoint(player.position):
                    self.teamOneMapping[player.playerName]['jungleAllyBotPresence'] += 1
                if self.jungleRedTopPresenceGrid.containsPoint(player.position):
                    self.teamOneMapping[player.playerName]['jungleEnemyTopPresence'] += 1
                if self.jungleRedBotPresenceGrid.containsPoint(player.position):
                    self.teamOneMapping[player.playerName]['jungleEnemyBotPresence'] += 1
            
            # For team two
            for player in snapshot.teams[1].players:
                if self.midLanePresenceGrid.containsPoint(player.position):
                    self.teamTwoMapping[player.playerName]['midLanePresence'] += 1
                if self.topLanePresenceGrid.containsPoint(player.position):
                    self.teamTwoMapping[player.playerName]['topLanePresence'] += 1
                if self.botLanePresenceGrid.containsPoint(player.position):
                    self.teamTwoMapping[player.playerName]['botLanePresence'] += 1

                if self.riverBotPresenceGrid.containsPoint(player.position):
                    self.teamTwoMapping[player.playerName]['riverBotPresence'] += 1
                if self.riverTopPresenceGrid.containsPoint(player.position):
                    self.teamTwoMapping[player.playerName]['riverTopPresence'] += 1

                if self.jungleBlueTopPresenceGrid.containsPoint(player.position):
                    self.teamTwoMapping[player.playerName]['jungleEnemyTopPresence'] += 1
                if self.jungleBlueBotPresenceGrid.containsPoint(player.position):
                    self.teamTwoMapping[player.playerName]['jungleEnemyBotPresence'] += 1
                if self.jungleRedTopPresenceGrid.containsPoint(player.position):
                    self.teamTwoMapping[player.playerName]['jungleAllyTopPresence'] += 1
                if self.jungleRedBotPresenceGrid.containsPoint(player.position):
                    self.teamTwoMapping[player.playerName]['jungleAllyBotPresence'] += 1
        
        for summonerName, mapping in self.teamOneMapping.items():
            for key in mapping.keys():
                mapping[key] /= l
        for summonerName, mapping in self.teamTwoMapping.items():
            for key in mapping.keys():
                mapping[key] /= l
            