from dataclasses import dataclass
from dataAnalysis.packages.Parsers.Separated.Events.LiteralTypes import ward_types

@dataclass
class WardPlacedGlobalRequest:
    role : str
    team : str
    side : str
    tournamentList : list[str]
    begTime : int
    endTime : int
    wardTypes : list[ward_types]