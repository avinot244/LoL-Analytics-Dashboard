from dataclasses import dataclass

@dataclass
class TeamSideRequest:
    seriesId : int
    gameNumber : int
    team : str