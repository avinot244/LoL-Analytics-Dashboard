import os
from tqdm import tqdm
import ujson
import pandas as pd
import csv

from dataAnalysis.packages.Parsers.Separated.Game.Snapshot import Snapshot
from dataAnalysis.packages.Parsers.Separated.Game.Player import Player
from dataAnalysis.packages.Parsers.Separated.Game.Team import Team
from dataAnalysis.packages.Parsers.Separated.Game.Stat import Stat
from dataAnalysis.packages.Parsers.Separated.Game.Item import Item

from dataAnalysis.packages.Parsers.Separated.Draft.DraftSnapshot import DraftSnapshot
from dataAnalysis.packages.Parsers.Separated.Draft.Ban import Ban
from dataAnalysis.packages.Parsers.Separated.Draft.TeamDraft import TeamDraft
from dataAnalysis.packages.Parsers.Separated.Draft.PlayerDraft import PlayerDraft

from dataAnalysis.packages.utils_stuff.Position import Position
from dataAnalysis.packages.utils_stuff.converter.champion import convertToChampionName, convertToChampionID


class SeparatedData:
    def __init__(self, root_dir : str = None,
                 gameSnapshotList : list[Snapshot] = None,
                 begGameTime : int = -1,
                 endGameTime : int = -1) -> None:
        self.winningTeam = -1

        if not(gameSnapshotList == None) and not(begGameTime == -1) and not(endGameTime == -1):
            self.gameSnapshotList = gameSnapshotList
            self.begGameTime = begGameTime
            self.endGameTime = endGameTime
            

        elif not(root_dir == None):
            self.gameSnapshotList : list[Snapshot] = list()
            self.begGameTime : int = 0
            self.endGameTime : int = 0
            self.draftSnapshotList : list[DraftSnapshot] = list()
            print("Parsing game snapshot files from root directory {}".format(root_dir))

            for subdir, _, files in os.walk(root_dir, topdown=True):
                l = lambda s : s[:-5]
                files = [l(f) for f in files]
                for file in tqdm(sorted(files, key=int)):
                    with open(os.path.join(subdir, file + ".json")) as f:
                        data = ujson.loads(f.read())
                    
                    df = pd.json_normalize(data)

                    if df['rfc461Schema'][0] == "stats_update":
                        teamPlayers : list[list[Player]] = [[],[]]
                        # Parsing players
                        for participant_dict in df['participants'][0]:
                            # Parsing goldStats of current participant
                            goldStats : dict = participant_dict["goldStats"]

                            # Parsing items of current participant
                            if "items" in participant_dict.keys():
                                tempItems : list[Item] = list()
                                for item_dict in participant_dict['items']:
                                    itemCooldown : float = item_dict['itemCooldown'] if "itemCooldown" in item_dict.keys() else -1
                                    itemID : int = item_dict["itemID"] if "itemID" in item_dict.keys() else -1
                                    itemStacks : int = item_dict["itemStacks"] if "itemStack" in item_dict.keys() else -1
                                    tempItems.append(Item(itemCooldown,itemID,itemStacks))
                            else :
                                tempItems = None
                            
                            # Parsing position of current participant
                            playerPosition : Position = Position(participant_dict["position"]["x"],
                                                                 participant_dict["position"]["z"])
                            tempStatDict : dict = dict()
                            # Parsing stats of current participant
                            for stat_dict in participant_dict["stats"]:
                                tempStatDict[stat_dict["name"]] = stat_dict["value"]

                            tempStat : Stat = Stat(tempStatDict["MINIONS_KILLED"],
                                                   tempStatDict["CHAMPIONS_KILLED"],
                                                   tempStatDict["NUM_DEATHS"],
                                                   tempStatDict["ASSISTS"],
                                                   tempStatDict["WARD_PLACED"],
                                                   tempStatDict["WARD_KILLED"],
                                                   tempStatDict["VISION_SCORE"],
                                                   tempStatDict["TOTAL_DAMAGE_DEALT"],
                                                   tempStatDict["TOTAL_DAMAGE_TAKEN"],
                                                   tempStatDict["TOTAL_DAMAGE_DEALT_TO_CHAMPIONS"],
                                                   tempStatDict["TOTAL_DAMAGE_SELF_MITIGATED"],
                                                   tempStatDict["TOTAL_DAMAGE_SHIELDED_ON_TEAMMATES"],
                                                   tempStatDict["TOTAL_HEAL_ON_TEAMMATES"],
                                                   tempStatDict["TOTAL_DAMAGE_DEALT_TO_BUILDINGS"],
                                                   tempStatDict["TOTAL_DAMAGE_DEALT_TO_OBJECTIVES"],
                                                   tempStatDict["TOTAL_TIME_CROWD_CONTROL_DEALT"],
                                                   tempStatDict["TIME_CCING_OTHERS"])

                            tempPlayer : Player = Player(participant_dict["championName"],
                                                         participant_dict["playerName"],
                                                         participant_dict["participantID"],
                                                         participant_dict["level"],
                                                         participant_dict["XP"],
                                                         participant_dict["attackDamage"],
                                                         participant_dict["attackSpeed"],
                                                         participant_dict["alive"],
                                                         participant_dict["health"],
                                                         participant_dict["healthRegen"],
                                                         participant_dict["magicResist"],
                                                         participant_dict["armor"],
                                                         participant_dict["armorPenetration"],
                                                         participant_dict["abilityPower"],
                                                         participant_dict["currentGold"],
                                                         participant_dict["totalGold"],
                                                         goldStats,
                                                         playerPosition,
                                                         tempItems,
                                                         tempStat)
                            if participant_dict["teamID"] == 100:
                                teamPlayers[0].append(tempPlayer)
                            elif participant_dict["teamID"] == 200:
                                teamPlayers[1].append(tempPlayer)
                        
                        # Parsing teams
                        i = 0
                        teams : list[Team] = []
                        for team_dict in df['teams'][0]:
                            tempTeam : Team = Team(team_dict["assists"],
                                                   team_dict["baronKills"],
                                                   team_dict["championsKills"],
                                                   team_dict["deaths"],
                                                   team_dict["dragonKills"],
                                                   team_dict["teamID"],
                                                   team_dict["inhibKills"],
                                                   team_dict["totalGold"],
                                                   team_dict["towerKills"],
                                                   teamPlayers[i])
                            teams.append(tempTeam)
                            i += 1
                        gameSnapshot : Snapshot = Snapshot(df["gameID"][0],
                                                           df["gameName"][0],
                                                           df["sequenceIndex"][0],
                                                           df["gameTime"][0],
                                                           df["platformID"],
                                                           teams)
                        self.gameSnapshotList.append(gameSnapshot)
                    elif df["rfc461Schema"][0] == "game_end":
                        if df["winningTeam"][0] == 100:
                            self.winningTeam = 0
                        elif df["winningTeam"][0] == 200:
                            self.winningTeam = 1
                    elif df["rfc461Schema"][0] == "champ_select":
                        # Parsing bans
                        tempBanList : list[Ban] = list()
                        for ban_dict in df["bannedChampions"][0]:
                            tempBanList.append(Ban(ban_dict["championID"],
                                                   ban_dict["teamID"]))
                        
                        # Parsing team/player picks
                        tempTeamDraft : list[TeamDraft] = list()
                        tempPlayerDraftList : list[PlayerDraft] = list()
                        # For team one:
                        for player_team_one_dict in df["teamOne"][0]:
                            tempPlayerDraft : PlayerDraft = PlayerDraft(player_team_one_dict["championID"],
                                                                        player_team_one_dict["summonerName"])
                            tempPlayerDraftList.append(tempPlayerDraft)
                        
                        tempTeamDraft.append(TeamDraft(tempPlayerDraftList))

                        tempPlayerDraftList : list[PlayerDraft] = list()
                        # For team two
                        for player_team_two_dict in df["teamTwo"][0]:
                            tempPlayerDraft : PlayerDraft = PlayerDraft(player_team_two_dict["championID"],
                                                                        player_team_two_dict["summonerName"])
                            tempPlayerDraftList.append(tempPlayerDraft)
                        
                        tempTeamDraft.append(TeamDraft(tempPlayerDraftList))
                        self.draftSnapshotList.append(DraftSnapshot(df["gameID"][0], 
                                                                    df["platformID"][0], 
                                                                    df["name"][0], 
                                                                    tempBanList,
                                                                    tempTeamDraft))

            if len(self.gameSnapshotList) > 0:
                self.endGameTime = self.gameSnapshotList[-1].gameTime
                self.playerPicks : list[PlayerDraft] = list()
                snapshot = self.gameSnapshotList[0]
                self.matchId = snapshot.gameName
                self.matchName = snapshot.gameName
                for i in range(2):
                    for j in range(5):
                        summonerName : str = snapshot.teams[i].players[j].playerName
                        championID : int = convertToChampionID(snapshot.teams[i].players[j].championName)
                        self.playerPicks.append(PlayerDraft(championID, summonerName))
            else:
                self.matchId = "Remake"
                self.playerPicks : list[PlayerDraft] = [PlayerDraft(-1, "")]
                
            # self.begGameTime = self.gameSnapshotList[0].gameTime
            self.matchName = ""
    
    def getPlayerList(self):
        firstGameSnapshot = self.gameSnapshotList[0]
        playersTeamOne : list[str] = firstGameSnapshot.teams[0].getPlayerList()
        playersTeamTwo : list[str] = firstGameSnapshot.teams[1].getPlayerList()
        return playersTeamOne, playersTeamTwo

    def getPlayerPositionHistory(self, participantID : int) -> list[Position]:
        positionList : list[Position] = list()  
        for gameSnapshot in self.gameSnapshotList:
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
    
    def getPlayerID(self, playerName : str) -> int:
        assert (playerName in self.gameSnapshotList[0].teams[0].getPlayerList()) or (playerName in self.gameSnapshotList[0].teams[1].getPlayerList())
        if playerName in self.gameSnapshotList[0].teams[0].getPlayerList():
            return self.gameSnapshotList[0].teams[0].getPlayerID(playerName)
        else:
            return self.gameSnapshotList[0].teams[1].getPlayerID(playerName)
 
    def splitData(self, gameDuration : int, splitList : list[int]):
        snapshotListTemp : list[list[Snapshot]] = [[] for _ in range(len(splitList))]
        res : list[SeparatedData] = list() # List of len 1+len(splitList)
        for snapshot in self.gameSnapshotList:
            snapshotTime = snapshot.convertGameTimeToSeconds(gameDuration, self.begGameTime, self.endGameTime)
            for i in range(len(splitList)):
                if snapshotTime < splitList[i]:
                    snapshotListTemp[i].append(snapshot)
                    break
        for snapshotLst in snapshotListTemp:
            res.append(SeparatedData(gameSnapshotList=snapshotLst, begGameTime=self.begGameTime, endGameTime=self.endGameTime))
        return res
    
    def getSnapShotByTime(self, time : float, gameDuration : int):
        """Gets snapshot where time is the closest"""
        begGameTime = self.begGameTime
        endGameTime = self.endGameTime

        firstSnapShotTime = self.gameSnapshotList[0].convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime)
        delta = abs(time - firstSnapShotTime)
        idx = 0
        for i in range(len(self.gameSnapshotList)):
            snapShotTime = self.gameSnapshotList[i].convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime)
            tempDelta = abs(time - snapShotTime)
            if tempDelta < delta:
                delta = tempDelta
                idx = i
        
        return self.gameSnapshotList[idx]
    
    def getTeamNames(self) -> dict:
        teamName : dict = dict()
        firstSnapShot = self.gameSnapshotList[0]
        teamNameOne = firstSnapShot.teams[0].players[0].playerName.split(' ')[0]
        teamNameTwo = firstSnapShot.teams[1].players[0].playerName.split(' ')[0]
        teamName[teamNameOne] = 0
        teamName[teamNameTwo] = 1
        return teamName


    def draftToCSV(self, path : str, new : bool, patch : str, seriesId : int, tournament : str, gameNumber : int, date : str, teamBlue : str, teamRed : str):
        draft : DraftSnapshot = self.draftSnapshotList[-1]
        # Asserting the right open option
        if new:
            open_option = 'w'
        else:
            open_option = 'a'

        # Writing the draft pick order database
        full_path = path  + "draft_pick_order.csv"
        with open(full_path, open_option) as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            if new:
                header = ["Date", "Tournament", "Patch", "SeriesId", "Winner", "GameNumber", "teamBlue", "teamRed", "BB1", "BB2", "BB3", "BB4", "BB5", "BP1", "BP2", "BP3", "BP4", "BP5", "RB1", "RB2", "RB3", "RB4", "RB5", "RP1", "RP2", "RP3", "RP4", "RP5"]
                writer.writerow(header)
            
            data : list = list()
            data.append(date)
            data.append(tournament)
            data.append(patch)
            data.append(seriesId)
            data.append(self.winningTeam)
            data.append(gameNumber)
            data.append(teamBlue)
            data.append(teamRed)

            if len(draft.bans) < 10:
                for _ in range(10-len(draft.bans)):
                    draft.bans.append(Ban(-1, -1))
                
            for i in range(2):
                if len(draft.teams[i].playerDraftList) < 5:
                    for _ in range(5-len(draft.teams[0].playerDraftList)):
                        draft.teams[i].playerDraftList.append(PlayerDraft(-1, ""))

            # Getting bans of blue side
            for i in range(5):
                data.append(convertToChampionName(draft.bans[2*i].championID))

            # Getting pick of blue side
            for i in range(len(draft.teams[0].playerDraftList)):
                data.append(convertToChampionName(draft.teams[0].playerDraftList[i].championID))
            
            # Getting bans for red side 
            for i in range(5):
                data.append(convertToChampionName(draft.bans[2*i + 1].championID))
            
            # Getting picks fo red side
            for i in range(len(draft.teams[1].playerDraftList)):
                data.append(convertToChampionName(draft.teams[1].playerDraftList[i].championID))
            writer.writerow(data)
        
        # Writing the draft player picks database
        full_path = path + "draft_player_picks.csv"
        with open(full_path, open_option) as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            data : list = list()
            if new :
                header = ["Date", "Tournament", "Patch", "SeriesId", "SummonnerName", "ChampionName", "Role", "GameNumber"]
                writer.writerow(header)

            for playerPick in self.playerPicks:
                if playerPick.summonerName != "" and playerPick.championID != -1 :
                    data.append(date)
                    data.append(tournament)
                    data.append(patch)
                    data.append(seriesId)
                    data.append(playerPick.summonerName)
                    data.append(convertToChampionName(playerPick.championID))

                    # Geting role
                    role : str = ""
                    participantID : int = self.gameSnapshotList[-1].teams[0].getPlayerID(playerPick.summonerName)
                    
                    if participantID != -1:
                        role = self.gameSnapshotList[-1].teams[0].getRole(playerPick.summonerName)
                    else:
                        role = self.gameSnapshotList[-1].teams[1].getRole(playerPick.summonerName)
                    
                    data.append(role)

                    data.append(gameNumber)

                    
                    
                    writer.writerow(data)
                    data = []
