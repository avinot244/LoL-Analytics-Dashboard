from dataclasses import dataclass

@dataclass
class PlayerPositionRequest:
    role : str
    side : str
    seriesId : int
    gameNumber : int
    begTime : int
    endTime : int