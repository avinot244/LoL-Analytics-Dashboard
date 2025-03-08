from dataclasses import dataclass

@dataclass
class TournamentListRequest:
    tournamentList : list[str]