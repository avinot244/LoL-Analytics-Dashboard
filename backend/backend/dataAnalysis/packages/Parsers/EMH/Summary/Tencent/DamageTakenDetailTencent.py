from dataclasses import dataclass

@dataclass
class DamageTakenDetailTencent:
    restoreLife: int
    damageTaken: float
    physicalDamageTaken: float
    magicalDamageTaken: float
    trueDamageTaken: float
    takenDamageRate: float
    highestTakenDamageRate: bool
    damageTakenPerGold: float
    damageTakenPerMinute: float