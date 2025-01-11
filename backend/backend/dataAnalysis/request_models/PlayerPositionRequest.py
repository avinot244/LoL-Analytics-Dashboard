from pydantic import BaseModel
from dataclasses import dataclass

@dataclass
class PlayerPositionRequest(BaseModel):
    playerName: str
    seriesIdList: list[int]
    begTime: int
    endTime: int