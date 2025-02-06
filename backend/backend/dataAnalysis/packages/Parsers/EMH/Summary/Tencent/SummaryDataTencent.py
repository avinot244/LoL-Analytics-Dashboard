import json

from dataAnalysis.packages.Parsers.EMH.Summary.Tencent.TeamEndGameStatTencent import TeamEndGameStatTencent
from dataAnalysis.packages.Parsers.EMH.Summary.Tencent.PlayerEndGameStatTencent import PlayerEndGameStatTencent
from dataAnalysis.packages.Parsers.EMH.Summary.Tencent.BattleDetailTencent import BattleDetailTencent
from dataAnalysis.packages.Parsers.EMH.Summary.Tencent.DamageDetailTencent import DamageDetailTencent
from dataAnalysis.packages.Parsers.EMH.Summary.Tencent.DamageTakenDetailTencent import DamageTakenDetailTencent
from dataAnalysis.packages.Parsers.EMH.Summary.Tencent.OtherDetailTencent import OtherDetailTencent
from dataAnalysis.packages.Parsers.EMH.Summary.Tencent.VisionDetailTencent import VisionDetailTencent


class SummaryDataTencent:
    def __init__(self, json_path : str):
        self.json_path = json_path
        
        
        with open(self.json_path) as f:
            data = json.loads(f.read())
            
        # Parsing global team info
        self.teams : list[TeamEndGameStatTencent] = []
        for teamDict in data["teamInfos"]:
            # parsing players
            players : list[PlayerEndGameStatTencent] = []
            for playerDict in teamDict["playerInfos"]:
                battleDetail = BattleDetailTencent(
                    kills=playerDict["battleDetail"]["kills"],
                    death=playerDict["battleDetail"]["death"],
                    assist=playerDict["battleDetail"]["assist"],
                    kda=playerDict["battleDetail"]["kda"],
                    highestKDA=playerDict["battleDetail"]["highestKDA"],
                    highestKillStreak=playerDict["battleDetail"]["highestKillStreak"],
                    highestMultiKill=playerDict["battleDetail"]["highestMultiKill"],
                    attendWarRate=playerDict["battleDetail"]["attendWarRate"],
                    highestAttendWarRate=playerDict["battleDetail"]["highestAttendWarRate"]
                )
                
                damageDetail = DamageDetailTencent(
                    heroDamage=playerDict["damageDetail"]["heroDamage"],
                    heroPhysicalDamage=playerDict["damageDetail"]["heroPhysicalDamage"],
                    heroMagicalDamage=playerDict["damageDetail"]["heroMagicalDamage"],
                    heroTrueDamage=playerDict["damageDetail"]["heroTrueDamage"],
                    totalDamage=playerDict["damageDetail"]["totalDamage"],
                    totalPhysicalDamage=playerDict["damageDetail"]["totalPhysicalDamage"],
                    totalMagicalDamage=playerDict["damageDetail"]["totalMagicalDamage"],
                    totalTrueDamage=playerDict["damageDetail"]["totalTrueDamage"],
                    highestCritDamage=playerDict["damageDetail"]["highestCritDamage"],
                    damageTransit=playerDict["damageDetail"]["damageTransit"],
                    highestDamageTransit=playerDict["damageDetail"]["highestDamageTransit"],
                    damagePerGold=playerDict["damageDetail"]["damagePerGold"],
                    highestDamagePerGold=playerDict["damageDetail"]["highestDamagePerGold"],
                    damageRate=playerDict["damageDetail"]["damageRate"],
                    highestDamageRate=playerDict["damageDetail"]["highestDamageRate"],
                    damagePerMinute=playerDict["damageDetail"]["damagePerMinute"],
                )
                
                damageTakenDetail = DamageTakenDetailTencent(
                    restoreLife=playerDict["DamageTakenDetail"]["restoreLife"],
                    damageTaken=playerDict["DamageTakenDetail"]["damageTaken"],
                    physicalDamageTaken=playerDict["DamageTakenDetail"]["physicalDamageTaken"],
                    magicalDamageTaken=playerDict["DamageTakenDetail"]["magicalDamageTaken"],
                    trueDamageTaken=playerDict["DamageTakenDetail"]["trueDamageTaken"],
                    takenDamageRate=playerDict["DamageTakenDetail"]["takenDamageRate"],
                    highestTakenDamageRate=playerDict["DamageTakenDetail"]["highestTakenDamageRate"],
                    damageTakenPerGold=playerDict["DamageTakenDetail"]["damageTakenPerGold"],
                    damageTakenPerMinute=playerDict["DamageTakenDetail"]["damageTakenPerMinute"]
                )
                
                otherDetail = OtherDetailTencent(
                    golds=playerDict["otherDetail"]["golds"],
                    oppositeGoldsDiff=playerDict["otherDetail"]["oppositeGoldsDiff"],
                    oppositeGoldsDiffAt15=playerDict["otherDetail"]["oppositeGoldsDiffAt15"],
                    turretAmount=playerDict["otherDetail"]["turretAmount"],
                    creepsKilled=playerDict["otherDetail"]["creepsKilled"],
                    deathTime=playerDict["otherDetail"]["deathTime"],
                    level=playerDict["otherDetail"]["level"],
                    firstBlood=playerDict["otherDetail"]["firstBlood"],
                    firstBloodAssists=playerDict["otherDetail"]["firstBloodAssists"],
                    firstTurret=playerDict["otherDetail"]["firstTurret"],
                    firstTurretKill=playerDict["otherDetail"]["firstTurretKill"],
                    firstTurretAssist=playerDict["otherDetail"]["firstTurretAssist"],
                    spentGold=playerDict["otherDetail"]["spentGold"],
                    totalNeutralMinKilled=playerDict["otherDetail"]["totalNeutralMinKilled"],
                    totalMinKilledYourJungle=playerDict["otherDetail"]["totalMinKilledYourJungle"],
                    totalMinKilledEnemyJungle=playerDict["otherDetail"]["totalMinKilledEnemyJungle"],
                    epicMonsterKills=playerDict["otherDetail"]["epicMonsterKills"],
                    mvp=playerDict["otherDetail"]["mvp"],
                    goldPercent=playerDict["otherDetail"]["goldPercent"]
                )
                
                visionDetail = VisionDetailTencent(
                    wardPlaced=playerDict["visionDetail"]["wardPlaced"],
                    wardKilled=playerDict["visionDetail"]["wardKilled"],
                    visionScore=playerDict["visionDetail"]["visionScore"],
                    highestVisionScore=playerDict["visionDetail"]["highestVisionScore"],
                    controlWardPurchased=playerDict["visionDetail"]["controlWardPurchased"]
                )
                                
                players.append(PlayerEndGameStatTencent(
                    playerId=playerDict["playerId"],
                    playerName=playerDict["playerName"],
                    playerLocation=playerDict["playerLocation"],
                    heroId=playerDict["heroId"],
                    spell1Name=playerDict["spell1Name"],
                    spell2Name=playerDict["spell2Name"],
                    minionKilled=playerDict["minionKilled"],
                    battleDetail=battleDetail,
                    damageDetail=damageDetail,
                    damageTakenDetail=damageTakenDetail,
                    otherDetail=otherDetail,
                    visionDetail=visionDetail
                ))
                
            # parsing global team stats
            self.teams.append(TeamEndGameStatTencent(
                teamId=teamDict["teamId"],
                dragonAmount=teamDict["dragonAmount"],
                baronAmount=teamDict["baronAmount"],
                elderDragonAmount=teamDict["elderDragonAmount"],
                riftHeraldAmount=teamDict["riftHeraldAmount"],
                voidGrubAmount=teamDict["voidGrubAmount"],
                turretAmount=teamDict["turretAmount"],
                golds=teamDict["golds"],
                playerInfos=players,
                isFirstRiftHerald=teamDict["isFirstRiftHerald"],
                isFirstInhibitor=teamDict["isFirstInhibitor"],
                isFirstTurret=teamDict["isFirstTurret"],
                baronIncome=teamDict["baronIncome"],
                baronIncomeTeamDiff=teamDict["baronIncomeTeamDiff"],
                inhibitKills=teamDict["inhibitKills"],
                teamSide=teamDict["teamSide"],
                isFirstDragon=teamDict["isFirstDragon"],
                dragonSpirit=teamDict["dragonSpirit"],
                dragonSpiritType=teamDict["dragonSpiritType"],
            ))
            
    def getDrakeCount(self, side : int) -> int:
        # Blue side : 0, red side : 1
        return self.teams[side].elderDragonAmount + self.teams[side].dragonAmount
    
    def getGrubsCount(self, side : int) -> int:
        # Blue side : 0, red side : 1
        return self.teams[side].voidGrubAmount