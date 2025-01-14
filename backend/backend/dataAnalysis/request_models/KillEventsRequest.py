from dataclasses import dataclass

@dataclass
class KillEventsRequest:
    seriesId : int
    gameNumber : int
    begTime : int
    endTime : int