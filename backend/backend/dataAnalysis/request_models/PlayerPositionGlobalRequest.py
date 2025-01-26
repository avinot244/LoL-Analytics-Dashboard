from dataclasses import dataclass

@dataclass
class PlayerPositionGlobalRequest:
    role : str
    side : str
    tournamentList : list[str]
    team : str
    begTime : int # Min of all the games
    endTime : int # Max of all the games