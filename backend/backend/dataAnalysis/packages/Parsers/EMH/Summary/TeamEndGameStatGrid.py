from dataAnalysis.packages.Parsers.EMH.Summary.ObjectiveGrid import ObjectiveGrid
from dataAnalysis.packages.Parsers.EMH.Summary.PlayerEndGameStatGrid import PlayerEndGameStatGrid

class TeamEndGameStatGrid:
    def __init__(
        self,
        id : str,
        name : str,
        score : int,
        won : bool,
        kills : int,
        killAssistsReceived : int, # Assists
        killAssistsGiven : int,
        deaths : int,
        structureDestroyed : int,
        objectives : list[ObjectiveGrid],
        players : list[PlayerEndGameStatGrid]
    ):
        self.id = id
        self.name = name
        self.score = score
        self.won = won,
        self.kills = kills,
        self.killAssistsReceived = killAssistsReceived
        self.killAssistsGiven = killAssistsGiven
        self.deaths = deaths
        self.structureDestroyed = structureDestroyed
        self.objectives = objectives
        self.players = players