from dataclasses import dataclass

@dataclass
class TeamDraftDataRequest:
    teamName : str
    tournamentList : list[str]
    side : str
    patch : str