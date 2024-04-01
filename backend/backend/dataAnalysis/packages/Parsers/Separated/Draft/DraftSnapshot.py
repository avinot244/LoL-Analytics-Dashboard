from Parsers.Separated.Draft.Ban import Ban
from Parsers.Separated.Draft.TeamDraft import TeamDraft

class DraftSnapshot:
    def __init__(self,
                 gameID : int,
                 platformID : str,
                 gameName : str,
                 bans : list[Ban],
                 teams : list[TeamDraft]) -> None:
        self.gameID = gameID
        self.platformID = platformID
        self.gameName = gameName
        self.bans = bans
        self.teams = teams