from dataclasses import dataclass

@dataclass
class GrubsDrakeStatsRequest:
    teamName : str
    tournamentList : list[str]