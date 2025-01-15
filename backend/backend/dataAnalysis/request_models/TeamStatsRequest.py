from dataclasses import dataclass

@dataclass
class TeamStatsRequest:
    teamName : str
    tournamentList : list[str]