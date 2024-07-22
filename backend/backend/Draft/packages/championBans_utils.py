from ..models import DraftPickOrder

import csv
import pandas as pd
import os
import math

def isChampionBanned(championName : str, tournament : str, patch : str, side : str) -> bool:
    queryDraftPickOrder = DraftPickOrder.objects.filter(tournament__exact=tournament, patch__contains=patch)
    for draftPickOrder in queryDraftPickOrder:
        blueBans = [
            draftPickOrder.bb1,
            draftPickOrder.bb2,
            draftPickOrder.bb3,
            draftPickOrder.bb4,
            draftPickOrder.bb5,
        ]
        redBans = [
            draftPickOrder.rb1,
            draftPickOrder.rb2,
            draftPickOrder.rb3,
            draftPickOrder.rb4,
            draftPickOrder.rb5,
        ]
        
        if (championName in blueBans) and side == "Blue":
            return True
        elif (championName in redBans) and side == "Red":
            return False
    return False

def getBanRateInfo(championName : str, tournament : str, patch : str, side : str) -> tuple[float, float, float]:
    queryDraftPickOrder = DraftPickOrder.objects.filter(tournament__exact=tournament, patch__contains=patch)

    banCounter1Rota : int = 0
    banCounter2Rota : int = 0
    totalTimesBaned : int = 0
    amountOfGames : int = len(queryDraftPickOrder)

    for draftBanOrder in queryDraftPickOrder:
        blueBans1Rota = [
            draftBanOrder.bb1,
            draftBanOrder.bb2,
            draftBanOrder.bb3
        ]
        blueBans2Rota = [
            draftBanOrder.bb4,
            draftBanOrder.bb5
        ]

        redBans1Rota = [
            draftBanOrder.rb1,
            draftBanOrder.rb2,
            draftBanOrder.rb3
        ]
        redBans2Rota = [
            draftBanOrder.rb4,
            draftBanOrder.rb5
        ]
        if (championName in blueBans1Rota) and side == "Blue":
            totalTimesBaned += 1
            banCounter1Rota += 1
        elif (championName in blueBans2Rota) and side == "Blue":
            totalTimesBaned += 1
            banCounter2Rota += 1
        elif (championName in redBans1Rota) and side == "Red":
            totalTimesBaned += 1
            banCounter1Rota += 1
        elif (championName in redBans2Rota) and side == "Red":
            totalTimesBaned += 1
            banCounter2Rota += 1
    
    if totalTimesBaned == 0:
        return (0, 0, 0)
    else:
        banRate : float = totalTimesBaned/amountOfGames
        banRate1Rota : float = banCounter1Rota/totalTimesBaned
        banRate2Rota : float = banCounter2Rota/totalTimesBaned

        return (banRate, banRate1Rota, banRate2Rota)
   
def isLineInDatabase(path : str, championName : str, patch : str, tournament : str, side : str) -> bool:
    df : pd.DataFrame = pd.read_csv(path, sep=";")

    if df.empty:
        return False
    else:
        for _, row in df.iterrows():
            if row["ChampionName"] == championName and str(row["Patch"]) == patch and row["Tournament"] == tournament and row["Side"] == side:
                return True

        return False   

def updateDatabase(path : str,
                   championName : str,
                   patch : str,
                   tournament : str,
                   side : str,
                   banRate : float,
                   banRate1Rota : float,
                   banRate2Rota : float,) -> None:
    df : pd.DataFrame = pd.read_csv(path, sep=";")
    for index, row in df.iterrows():
        # Getting the line we want

        if row["ChampionName"] == championName and str(row["Patch"]) == patch and row["Tournament"] == tournament and row["Side"] == side:
            # If input data is different than csv data
            if not(abs(row["GlobalBanRate"] - banRate) < 0.01
                   and abs(row["BanRate1Rota"] - banRate1Rota) < 0.01
                   and abs(row["BanRate2Rota"] - banRate2Rota) < 0.01):
                
                df.at[index, "GlobalBanRate"] = banRate
                df.at[index, "BanRate1Rota"] = banRate1Rota
                df.at[index, "BanRate2Rota"] = banRate2Rota

                os.remove(path)
                df.to_csv(path, sep=";", index=False)
                break

def saveChampionBanStatsCSV(path : str,
                            new : bool,
                            championName : str,
                            patch : str,
                            tournament : str,
                            side : str,
                            banRate : float,
                            banRate1Rota : float,
                            banRate2Rota : float) -> None:
    if new:
        write_option : str = "w"
    else:
        write_option : str = "a"
    
    csv_file = open(path, write_option)
    writer = csv.writer(csv_file, delimiter=";")
    
    if new:
        header = ["ChampionName", "Patch", "Tournament", "Side", "GlobalBanRate", "BanRate1Rota", "BanRate2Rota"]
        writer.writerow(header)
        
        data = [championName, patch, tournament, side, banRate, banRate1Rota, banRate2Rota]
        writer.writerow(data)
        csv_file.close()
    elif isLineInDatabase(path, championName, patch, tournament):
        csv_file.close()
        updateDatabase(
            path,
            championName,
            patch,
            tournament,
            side,
            banRate,
            banRate1Rota,
            banRate2Rota
        )
    else:
        data = [championName, patch, tournament, side, banRate, banRate1Rota, banRate2Rota]

        writer.writerow(data)

        csv_file.close()