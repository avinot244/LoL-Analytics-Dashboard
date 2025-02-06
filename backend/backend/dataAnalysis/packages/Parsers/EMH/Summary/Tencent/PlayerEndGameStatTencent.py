from dataclasses import dataclass

from dataAnalysis.packages.Parsers.EMH.Summary.Tencent.BattleDetailTencent import BattleDetailTencent
from dataAnalysis.packages.Parsers.EMH.Summary.Tencent.DamageDetailTencent import DamageDetailTencent
from dataAnalysis.packages.Parsers.EMH.Summary.Tencent.DamageTakenDetailTencent import DamageTakenDetailTencent
from dataAnalysis.packages.Parsers.EMH.Summary.Tencent.OtherDetailTencent import OtherDetailTencent
from dataAnalysis.packages.Parsers.EMH.Summary.Tencent.VisionDetailTencent import VisionDetailTencent

@dataclass
class PlayerEndGameStatTencent:
    playerId : int
    playerName : str
    playerLocation : str
    heroId : int
    spell1Name : str
    spell2Name : str
    minionKilled : int
    battleDetail : BattleDetailTencent
    damageDetail : DamageDetailTencent
    damageTakenDetail : DamageTakenDetailTencent
    otherDetail : OtherDetailTencent
    visionDetail : VisionDetailTencent