import json
import pandas as pd

from dataAnalysis.packages.Parsers.EMH.Summary.PlayerEndGameStat import PlayerEndGameStat
from dataAnalysis.packages.Parsers.EMH.Summary.TeamEndGameStat import TeamEndGameStat
from dataAnalysis.packages.Parsers.EMH.Summary.Ban import Ban
from dataAnalysis.packages.Parsers.EMH.Summary.Objective import Objective


class SummaryData:
    def __init__(self, json_path : str) -> None:
        self.json_path = json_path
        self.tencentData = False
        try:
            with open(json_path) as f:
                data = json.loads(f.read())
                df = pd.json_normalize(data)

                self.patch : str = df["gameVersion"][0]
        except:
            self.tencentData = True
        
        if not(self.tencentData):
            df = pd.json_normalize(data)

            self.patch : str = df["gameVersion"][0]
            self.gameCreation : int = df['gameCreation'][0]
            self.gameDuration : int = df['gameDuration'][0]
            self.gameEndTimestamp : int = df['gameEndTimestamp'][0]
            self.gameId : int = df['gameId'][0]
            self.gameMode : str = df['gameMode'][0]
            self.gameName : str = df['gameName'][0]
            self.gameStartTimestamp : int = df['gameStartTimestamp'][0]
            self.gameType : str = df['gameType'][0]
            self.gameVersion : str = df['gameVersion'][0]
            self.mapId : int = df['mapId'][0]

            self.participants : list[PlayerEndGameStat] = list()

            self.platformId : str = df['platformId'][0]
            self.queueId : int = df['queueId'][0]
            self.seasonId : int = df['seasonId'][0]
            
            self.teams : list[TeamEndGameStat] = list()

            self.tournamentCode : str = df['tournamentCode'][0]

            for participant in df['participants'][0]:
                participantEndGameStat = PlayerEndGameStat(
                    participant['allInPings'],
                    participant['assistMePings'],
                    participant['assists'],
                    participant['baronKills'],
                    participant['basicPings'],
                    participant['bountyLevel'],
                    participant['champExperience'],
                    participant['champLevel'],
                    participant['championId'],
                    participant['championName'],
                    participant['championTransform'],
                    participant['commandPings'],
                    participant['consumablesPurchased'],
                    participant['damageDealtToBuildings'],
                    participant['damageDealtToObjectives'],
                    participant['damageDealtToTurrets'],
                    participant['damageSelfMitigated'],
                    participant['dangerPings'],
                    participant['deaths'],
                    participant['detectorWardsPlaced'],
                    participant['doubleKills'],
                    participant['dragonKills'],
                    participant['eligibleForProgression'],
                    participant['enemyMissingPings'],
                    participant['enemyVisionPings'],
                    participant['firstBloodAssist'],
                    participant['firstBloodKill'],
                    participant['firstTowerAssist'],
                    participant['firstTowerKill'],
                    participant['gameEndedInEarlySurrender'],
                    participant['gameEndedInSurrender'],
                    participant['getBackPings'],
                    participant['goldEarned'],
                    participant['goldSpent'],
                    participant['holdPings'],
                    participant['individualPosition'],
                    participant['inhibitorKills'],
                    participant['inhibitorTakedowns'],
                    participant['inhibitorsLost'],
                    participant['item0'],
                    participant['item1'],
                    participant['item2'],
                    participant['item3'],
                    participant['item4'],
                    participant['item5'],
                    participant['item6'],
                    participant['itemsPurchased'],
                    participant['killingSprees'],
                    participant['kills'],
                    participant['lane'],
                    participant['largestCriticalStrike'],
                    participant['largestKillingSpree'],
                    participant['largestMultiKill'],
                    participant['longestTimeSpentLiving'],
                    participant['magicDamageDealt'],
                    participant['magicDamageDealtToChampions'],
                    participant['magicDamageTaken'],
                    participant['needVisionPings'],
                    participant['neutralMinionsKilled'],
                    participant['nexusKills'],
                    participant['nexusLost'],
                    participant['nexusTakedowns'],
                    participant['objectivesStolen'],
                    participant['objectivesStolenAssists'],
                    participant['onMyWayPings'],
                    participant['participantId'],
                    participant['pentaKills'],
                    participant['physicalDamageDealt'],
                    participant['physicalDamageDealtToChampions'],
                    participant['physicalDamageTaken'],
                    participant['placement'],
                    participant['playerAugment1'],
                    participant['playerAugment2'],
                    participant['playerAugment3'],
                    participant['playerAugment4'],
                    participant['playerSubteamId'],
                    participant['profileIcon'],
                    participant['pushPings'],
                    participant['quadraKills'],
                    participant['role'],
                    participant['sightWardsBoughtInGame'],
                    participant['spell1Casts'],
                    participant['spell1Id'],
                    participant['spell2Casts'],
                    participant['spell2Id'],
                    participant['spell3Casts'],
                    participant['spell4Casts'],
                    participant['subteamPlacement'],
                    participant['summoner1Casts'],
                    participant['summoner2Casts'],
                    participant['summonerId'],
                    participant['summonerLevel'],
                    participant['summonerName'],
                    participant['teamEarlySurrendered'],
                    participant['teamId'],
                    participant['teamPosition'],
                    participant['timeCCingOthers'],
                    participant['timePlayed'],
                    participant['totalAllyJungleMinionsKilled'],
                    participant['totalDamageDealt'],
                    participant['totalDamageDealtToChampions'],
                    participant['totalDamageShieldedOnTeammates'],
                    participant['totalDamageTaken'],
                    participant['totalEnemyJungleMinionsKilled'],
                    participant['totalHeal'],
                    participant['totalHealsOnTeammates'],
                    participant['totalMinionsKilled'],
                    participant['totalTimeCCDealt'],
                    participant['totalTimeSpentDead'],
                    participant['totalUnitsHealed'],
                    participant['tripleKills'],
                    participant['trueDamageDealt'],
                    participant['trueDamageDealtToChampions'],
                    participant['trueDamageTaken'],
                    participant['turretKills'],
                    participant['turretTakedowns'],
                    participant['turretsLost'],
                    participant['unrealKills'],
                    participant['visionClearedPings'],
                    participant['visionScore'],
                    participant['visionWardsBoughtInGame'],
                    participant['wardsKilled'],
                    participant['wardsPlaced'],
                    participant['win']
                )
                self.participants.append(participantEndGameStat)
            
            for team in df['teams'][0]:
                bans = team['bans']
                objectives  : dict = team['objectives']
                
                banList : list[Ban] = list()
                for ban in bans :
                    banObject = Ban(ban['championId'],
                                    ban['pickTurn'])
                    banList.append(banObject)
                
                objectiveList : list[Objective] = list()
                for objectiveName, objectiveStat in objectives.items():
                    objectiveObject = Objective(
                        objectiveName,
                        objectiveStat['first'],
                        objectiveStat['kills']
                    )
                    objectiveList.append(objectiveObject)
                
                teamObject = TeamEndGameStat(
                    banList, objectiveList,
                    team['teamId'],
                    team['win']
                )
                self.teams.append(teamObject)
            
    def getObjectiveCount(self, side : int, objectiveName : str) -> int:
        # Blue side : 0, red side : 1
        if not(self.tencentData):
            objectiveObject : Objective
            for objectiveObject in self.teams[side].objectives:
                if objectiveObject.objectiveName == objectiveName:
                    return objectiveObject.kills
            

        else:
            (seriesId, gameNumber) = (
                "/".join(self.json_path.split(".")[:-1]).split("/")[-1].split("_")[4],
                "/".join(self.json_path.split(".")[:-1]).split("/")[-1].split("_")[5]
            )
            path : str = "/".join(self.json_path.split("/")[:-1]) + "/end_state_" + seriesId + "_grid.json"
            with open(path) as f:
                data = json.loads(f.read())
            
            objectives : list[dict] = data["teams"][side]["objectives"]
            cpt : int = 0
            for objective_dict in objectives:
                if objectiveName == "dragon":
                    if "Drake" in objective_dict["id"]:
                        cpt += objective_dict["completionCount"]
                elif objectiveName == "horde":
                    if "VoidGrub" in objective_dict["id"]:
                        cpt += objective_dict["completionCount"]
            
            return cpt