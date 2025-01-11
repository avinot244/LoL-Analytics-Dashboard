from dataclasses import dataclass

@dataclass
class PlayerPositionRequest:
    playerName : str
    seriesId : int
    gameNumber : int
    begTime : int
    endTime : int