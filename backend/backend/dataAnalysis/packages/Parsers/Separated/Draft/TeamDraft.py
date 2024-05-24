from dataAnalysis.packages.Parsers.Separated.Draft.PlayerDraft import PlayerDraft

class TeamDraft:
    def __init__(self,
                 playerDraftList : list[PlayerDraft]) -> None:
        self.playerDraftList = playerDraftList