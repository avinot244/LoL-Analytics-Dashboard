import re

from dataAnalysis.packages.Parsers.Separated.Game.Player import Player
from dataAnalysis.packages.utils_stuff.Position import Position
from dataAnalysis.packages.utils_stuff.Computation.computation import *
from dataAnalysis.packages.api_calls.GRID.api_calls import get_team_info_from_seriesId, get_team_members_from_id

from dataAnalysis.globals import ROLE_LIST

class Team:
    def __init__(
        self,
        assists : int,
        baronKills : int,
        championKills : int,
        deaths : int,
        dragonKills : int,
        teamID : int,
        inhibKills : int,
        totalGold : int,
        towerKills : int,
        players : list[Player]
    ) -> None:
        self.assists = assists
        self.baronKills = baronKills
        self.championKills = championKills
        self.deaths = deaths
        self.dragonKills = dragonKills
        self.teamID = teamID
        self.inhibKills = inhibKills
        self.totalGold = totalGold
        self.towerKills = towerKills
        self.players = players

    def getPlayerNameFromID(self, participantID : int):
        for player in self.players:
            if player.participantID == participantID:
                return player.playerName
    
    def getPlayerList(self):
        playerList : list[str] = list()
        for player in self.players:
            playerList.append(player.playerName)
        return playerList
    
    def isPlayerInTeam(self, participantID):
        for player in self.players:
            if player.participantID == participantID:
                return True
        return False
    
    def getPlayerIdx(self, participantID):
        i : int = 0
        for player in self.players:
            if player.participantID == participantID:
                return i
            i += 1

    def getPlayerPosition(self, playerIdx : int) -> Position:
        return self.players[playerIdx].position
    
    def getPlayerID(self, playerName) -> int:
        for player in self.players:
            if player.playerName == playerName:
                return player.participantID
        return -1
    
    def getTeamName(self, seriesId : int) -> str:
        teamDict : dict = get_team_info_from_seriesId(seriesId)
        
        teamIdList : list = list(teamDict.keys())
        teamNameList : list = list(teamDict.values())
        playerListTeam2 : list = get_team_members_from_id(teamIdList[1])

        playerName : str = self.players[0].playerName
        for player in playerListTeam2:
            x = re.search(player, playerName)
            if x != None:
                return teamNameList[1]
        return teamNameList[0]

    def getClosesPlayerToJungler(self) -> Player:
        jungle = self.players[1]
        dist = abs_dist(jungle.position, self.players[0].position)
        idx = 0
        for i in range(len(self.players)):
            if i != 1:
                distTemp = abs_dist(jungle.position, self.players[i].position)
                if distTemp < dist:
                    dist = distTemp
                    idx = i
        return self.players[idx]

    def getClosestPlayer(self, player : Player) -> Player:
        idx_ = self.getPlayerIdx(self.getPlayerID(player.playerName))
        
        if idx_ > 0:
            res_idx = idx_ - 1
        else:
            res_idx = idx_ + 1
        
        dist = abs_dist(player.position, self.players[res_idx].position)
        
        for i in range(len(self.players)):
            if i != idx_:
                distTemp = abs_dist(player.position, self.players[i].position)
                if distTemp < dist:
                    dist = distTemp
                    res_idx = i
        return self.players[res_idx]
                
    
    def getRole(self, summonnerName : str):
        playerId : int = self.getPlayerID(summonnerName)
        playerIdx : int = self.getPlayerIdx(playerId)
        return ROLE_LIST[playerIdx]