from .Parsers.Separated.Game.Snapshot import Snapshot
from .Parsers.Separated.Game.Player import Player

class GameStat:
    def __init__(self, 
                 snapShot : Snapshot = None,
                 gameDuration : int = None,
                 begGameTime : int = None,
                 endGameTime : int = None):
        
        
        
        self.time = float(snapShot.convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime)/60)
        self.playerXPDiff : list[float] = list()
        self.playerCSDiff : list[float] = list()
        self.playerGoldDiff : list[float] = list()
        self.teamGoldDiff : float = 0

        for i in range(5):
            playerOne : Player = snapShot.teams[0].players[i]
            playerTwo : Player = snapShot.teams[1].players[i]

            self.playerXPDiff.append(playerOne.XPdiff(playerTwo))
            self.playerCSDiff.append(playerOne.CSdiff(playerTwo))
            self.playerGoldDiff.append(playerOne.goldDiff(playerTwo))

        self.teamGoldDiff = snapShot.goldDiff()
        
