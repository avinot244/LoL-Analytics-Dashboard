from dataclasses import dataclass

@dataclass
class DamageDetailTencent:
    heroDamage: float
    heroPhysicalDamage: float
    heroMagicalDamage: float
    heroTrueDamage: float
    totalDamage: float
    totalPhysicalDamage: float
    totalMagicalDamage: float
    totalTrueDamage: float
    highestCritDamage: int
    damageTransit: float
    highestDamageTransit: bool
    damagePerGold: float
    highestDamagePerGold: bool
    damageRate: float
    highestDamageRate: bool
    damagePerMinute: int