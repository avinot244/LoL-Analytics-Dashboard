from dataclasses import dataclass

@dataclass
class OtherDetailTencent:
    golds: int
    oppositeGoldsDiff: int
    oppositeGoldsDiffAt15: int
    turretAmount: int
    creepsKilled: int
    deathTime: int
    level: int
    firstBlood: bool
    firstBloodAssists: bool
    firstTurret: bool
    firstTurretKill: bool
    firstTurretAssist: bool
    spentGold: int
    totalNeutralMinKilled: int
    totalMinKilledYourJungle: int
    totalMinKilledEnemyJungle: int
    epicMonsterKills: int
    mvp: bool
    goldPercent: float