from dataclasses import dataclass
from dataAnalysis.packages.Parsers.Separated.Events.LiteralTypes import ward_types

@dataclass
class WardPlacedRequest:
    role : str
    side : str
    seriesId : int
    gameNumber : int
    begTime : int
    endTime : int
    wardTypes : list[ward_types]