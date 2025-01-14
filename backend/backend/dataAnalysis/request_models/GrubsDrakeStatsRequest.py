from dataclasses import dataclass

@dataclass
class GrubsDrakeStatsRequest:
    teamName : str
    tournament : str
    grubsCount : int
    drakeCount : int