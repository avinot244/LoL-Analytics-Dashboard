def getChampionWinRate(championName : str, tournament : str, patch : str) -> float:
    return 0

def getPickRateInfo(championName : str, tournament : str, patch : str) -> tuple[float, float, float]:
    return (0, 0, 0)

def getBanRateInfo(championName : str, tournament : str, patch : str) -> tuple[float, float, float]:
    return (0, 0, 0)

def getPickPosition(championName : str, tournament : str, patch : str) -> int:
    return 0

def getBlindPick(championName : str, tournament : str, patch : str) -> float:
    return 0


def saveChampionDraftStatsCSV(path : str,
                              new : bool,
                              winRate : float,
                              pickRate : float,
                              pickRate1Rota : float,
                              pickRate2Rota : float,
                              banRate : float,
                              banRate1Rota : float,
                              banRate2Rota : float,
                              mostPopularPickOrder : int,
                              blindPick : float) -> None:
    print("Saving to database")

def updateChampionDraftStatsSQLite(winRate : float,
                                   pickRate : float,
                                   pickRate1Rota : float,
                                   pickRate2Rota : float,
                                   banRate : float,
                                   banRate1Rota : float,
                                   banRate2Rota : float,
                                   mostPopularPickOrder : int,
                                   blindPick : float) -> None:
    print("updating SQLite database")
