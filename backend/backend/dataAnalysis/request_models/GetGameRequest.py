from dataclasses import dataclass

@dataclass
class GetGameRequest:
    team : str
    tournaments : list[str]