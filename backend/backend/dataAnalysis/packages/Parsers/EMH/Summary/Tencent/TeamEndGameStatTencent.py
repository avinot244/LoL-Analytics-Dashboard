from dataAnalysis.packages.Parsers.EMH.Summary.Tencent.PlayerEndGameStatTencent import PlayerEndGameStatTencent
from dataclasses import dataclass
from typing import List

@dataclass
class TeamEndGameStatTencent:
    teamId: int
    baronAmount: int
    dragonAmount: int
    elderDragonAmount: int
    riftHeraldAmount: int
    voidGrubAmount: int
    turretAmount: int
    golds: int
    playerInfos: List[PlayerEndGameStatTencent]
    isFirstRiftHerald: bool
    isFirstInhibitor: bool
    isFirstTurret: bool
    baronIncome: List[int]
    baronIncomeTeamDiff: List[int]
    inhibitKills: int
    teamSide: str
    isFirstDragon: bool
    dragonSpirit: bool
    dragonSpiritType: str