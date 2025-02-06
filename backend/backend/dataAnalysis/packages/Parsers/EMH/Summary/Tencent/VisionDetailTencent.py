from dataclasses import dataclass

@dataclass
class VisionDetailTencent:
    wardPlaced: int
    wardKilled: int
    visionScore: float
    highestVisionScore: bool
    controlWardPurchased: int