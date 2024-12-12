from dataAnalysis.packages.Parsers.EMH.Summary.AssistObject import AssistObject
from dataAnalysis.packages.Parsers.EMH.Summary.ObjectiveGrid import ObjectiveGrid

class PlayerEndGameStatGrid:
    def __init__(
        self,
        id : str,
        name : str,
        kills : int,
        killsAssistsReceived : int,
        killAssistsGiven : int,
        killAssistsReceivedFromPlayer : list[AssistObject],
        deaths : int,
        structuredDestroyed : int,
        objectives : list[ObjectiveGrid],
    ):
        self.id = id
        self.name = name
        self.kills = kills
        self.killsAssistsReceived = killsAssistsReceived
        self.killAssistsGiven = killAssistsGiven
        self.killAssistsReceivedFromPlayer = killAssistsReceivedFromPlayer
        self.deaths = deaths,
        self.structuredDestroyed = structuredDestroyed
        self.objectives = objectives