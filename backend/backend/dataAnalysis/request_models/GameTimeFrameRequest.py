from dataclasses import dataclass

@dataclass
class GameTimeFrameRequest:
    seriesId : int
    gameNumber : int
    begTime : int
    endTime : int