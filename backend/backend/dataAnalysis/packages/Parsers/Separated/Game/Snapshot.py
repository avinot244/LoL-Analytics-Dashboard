from dataAnalysis.packages.Parsers.Separated.Game.Team import Team

class Snapshot:
    def __init__(self,
                 gameID : int,
                 gameName : str,
                 seqIdx : int,
                 gameTime : int,
                 platformID : str,
                 teams : list[Team]):
        self.gameID = gameID
        self.gameName = gameName
        self.seqIdx = seqIdx
        self.gameTime = gameTime
        self.platformID = platformID
        self.teams = teams

    def convertGameTimeToSeconds(self, gameDuration : int, begGameTime : int, endGameTime : int):
        return ((self.gameTime - begGameTime)*gameDuration)/(endGameTime - begGameTime)
    
    def goldDiff(self):
        return self.teams[0].totalGold - self.teams[1].totalGold