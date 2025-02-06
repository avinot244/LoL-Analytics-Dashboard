from dataclasses import dataclass

@dataclass
class BattleDetailTencent:
    kills: int
    death: int
    assist: int
    kda: float
    highestKDA: bool
    highestKillStreak: int
    highestMultiKill: int
    attendWarRate: float
    highestAttendWarRate: bool