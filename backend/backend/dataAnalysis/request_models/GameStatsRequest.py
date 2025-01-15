from dataclasses import dataclass

@dataclass
class GameStatsRequest:
    seriesId : int
    gameNumber : int