from ..models import DraftPlayerPick, DraftPickOrder, ChampionDraftStats

import csv
import pandas as pd
import os
import math

def isChampionPicked(championName : str, tournament : str, patch : str, side : str) -> bool:
    queryDraftPickOrder = DraftPickOrder.objects.filter(tournament__exact=tournament, patch__contains=patch)
    for draftPickOrder in queryDraftPickOrder:
        bluePicks = [
            draftPickOrder.bp1,
            draftPickOrder.bp2,
            draftPickOrder.bp3,
            draftPickOrder.bp4,
            draftPickOrder.bp5
        ]
        redPick = [
            draftPickOrder.rp1,
            draftPickOrder.rp2,
            draftPickOrder.rp3,
            draftPickOrder.rp4,
            draftPickOrder.rp5
        ]
        if (championName in bluePicks) and side == "Blue":
            return True
        elif (championName in redPick) and side == "Red":
            return True
    return False


def getChampionWinRate(championName : str, tournament : str, patch : str, side : str) -> float:
    queryDraftPickOrder = DraftPickOrder.objects.filter(tournament__exact=tournament, patch__contains=patch)
    gameWinCounter : int = 0
    amountOfGames : int = 0
    for draftPickOrder in queryDraftPickOrder:
        bluePicks = [
            draftPickOrder.bp1,
            draftPickOrder.bp2,
            draftPickOrder.bp3,
            draftPickOrder.bp4,
            draftPickOrder.bp5
        ]
        redPick = [
            draftPickOrder.rp1,
            draftPickOrder.rp2,
            draftPickOrder.rp3,
            draftPickOrder.rp4,
            draftPickOrder.rp5
        ]
        if (championName in bluePicks) and side == "Blue":
            amountOfGames += 1
        elif (championName in redPick) and side == "Red":
            amountOfGames += 1
        
        if (championName in bluePicks) and draftPickOrder.winner == 0 and side == "Blue":
            gameWinCounter += 1
        elif (championName in redPick) and draftPickOrder.winner == 1 and side == "Red":
            gameWinCounter += 1
        
        
    winRate : float = gameWinCounter/amountOfGames

    return winRate

def getPickRateInfo(championName : str, tournament : str, patch : str, side : str) -> tuple[float, float, float]:
    queryDraftPickOrder = DraftPickOrder.objects.filter(tournament__exact=tournament, patch__contains=patch)

    pickCounter1Rota : int = 0
    pickCounter2Rota : int = 0
    totalTimesPicked : int = 0
    amountOfGames : int = len(queryDraftPickOrder)

    for draftPickOrder in queryDraftPickOrder:
        bluePicks1Rota = [
            draftPickOrder.bp1,
            draftPickOrder.bp2,
            draftPickOrder.bp3
        ]
        bluePicks2Rota = [
            draftPickOrder.bp4,
            draftPickOrder.bp5
        ]

        redPicks1Rota = [
            draftPickOrder.rp1,
            draftPickOrder.rp2,
            draftPickOrder.rp3
        ]
        redPicks2Rota = [
            draftPickOrder.rp4,
            draftPickOrder.rp5
        ]
        if (championName in bluePicks1Rota) and side == "Blue":
            totalTimesPicked += 1
            pickCounter1Rota += 1
        elif (championName in bluePicks2Rota) and side == "Blue":
            totalTimesPicked += 1
            pickCounter2Rota += 1
        elif (championName in redPicks1Rota) and side == "Red":
            totalTimesPicked += 1
            pickCounter1Rota += 1
        elif (championName in redPicks2Rota) and side == "Red":
            totalTimesPicked += 1
            pickCounter2Rota += 1
    
    if totalTimesPicked == 0:
        return (0, 0, 0)
    else:
        pickRate : float = totalTimesPicked/amountOfGames
        pickRate1Rota : float = pickCounter1Rota/totalTimesPicked
        pickRate2Rota : float = pickCounter2Rota/totalTimesPicked

    return (pickRate, pickRate1Rota, pickRate2Rota)

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

def getMostPopularPickPosition(championName : str, tournament : str, patch : str, side : str) -> int:
    queryDraftPickOrder = DraftPickOrder.objects.filter(tournament__exact=tournament, patch__contains=patch)

    pickPositionList : list = [0, 0, 0, 0, 0]
    for draftPickOrder in queryDraftPickOrder:
        if side == "Blue":
            if (championName == draftPickOrder.bp1):
                pickPositionList[0] += 1
            elif championName == draftPickOrder.bp2:
                pickPositionList[1] += 1
            elif championName == draftPickOrder.bp3:
                pickPositionList[2] += 1
            elif championName == draftPickOrder.bp4:
                pickPositionList[3] += 1
            elif championName == draftPickOrder.bp5:
                pickPositionList[4] += 1
        elif side == "Red":
            if (championName == draftPickOrder.rp1):
                pickPositionList[0] += 1
            elif championName == draftPickOrder.rp2:
                pickPositionList[1] += 1
            elif championName == draftPickOrder.rp3:
                pickPositionList[2] += 1
            elif championName == draftPickOrder.rp4:
                pickPositionList[3] += 1
            elif championName == draftPickOrder.rp5:
                pickPositionList[4] += 1
    
    (index, max) = (0, pickPositionList[0])
    for i, v in enumerate(pickPositionList):
        if v > max:
            max = v
            index = i
        
    return index

def isBlind(pickPosition : int, role : str, enemyRoleList : list, side : str) -> bool:
    if side == "Blue":
        if pickPosition == 0:
            return True
        elif pickPosition == 1 or pickPosition == 2:
            return not(role in enemyRoleList[:2])
        elif pickPosition == 3 or pickPosition == 4:
            return not(role in enemyRoleList[:3])
    elif side == "Red":
        if pickPosition == 0 or pickPosition == 1:
            return not(role in enemyRoleList[:1])
        elif pickPosition == 2:
            return not(role in enemyRoleList[:3])
        elif pickPosition == 3:
            return not(role in enemyRoleList[:3])
        elif pickPosition == 4:
            return False

def getPickPosition(championName : str, draftPickOrder : DraftPickOrder, side : str) -> int:
    if side == "Blue":
        if championName == draftPickOrder.bp1:
            return 0
        elif championName == draftPickOrder.bp2:
            return 1
        elif championName == draftPickOrder.bp3:
            return 2
        elif championName == draftPickOrder.bp4:
            return 3
        elif championName == draftPickOrder.bp5:
            return 4
    elif side == "Red":
        if championName == draftPickOrder.rp1:
            return 0
        elif championName == draftPickOrder.rp2:
            return 1
        elif championName == draftPickOrder.rp3:
            return 2
        elif championName == draftPickOrder.rp4:
            return 3
        elif championName == draftPickOrder.rp5:
            return 4

def getRoleForBlind(championName : str, queryPlayerPicks) -> str:
    for playerPick in queryPlayerPicks:
        if championName == playerPick.championName:
            return playerPick.role

def getEnemyRoleList(draftPickOrder : DraftPickOrder, queryPlayerPicks, side : str) -> list:
    roleList : list = list()
    if side == "Blue":
        championList : list = [
            draftPickOrder.rp1,
            draftPickOrder.rp2,
            draftPickOrder.rp3,
            draftPickOrder.rp4,
            draftPickOrder.rp5
        ]
        for championName in championList:
            playerPick : DraftPlayerPick = queryPlayerPicks.get(championName__exact=championName)
            roleList.append(playerPick.role)
        
    elif side == "Red":
        championList : list = [
            draftPickOrder.bp1,
            draftPickOrder.bp2,
            draftPickOrder.bp3,
            draftPickOrder.bp4,
            draftPickOrder.bp5
        ]
        for championName in championList:
            playerPick : DraftPlayerPick = queryPlayerPicks.get(championName__exact=championName)
            roleList.append(playerPick.role)

    return roleList

def getBlindPick(championName : str, tournament : str, patch : str, side : str) -> float:
    queryDraftPickOrder = DraftPickOrder.objects.filter(tournament__exact=tournament, patch__contains=patch)

    counterBlinded : int = 0
    amountOfGames = len(queryDraftPickOrder)
    for draftPickOrder in queryDraftPickOrder:
        queryPlayerPicks = DraftPlayerPick.objects.filter(seriesId__exact=draftPickOrder.seriesId,tournament__exact=tournament, patch__contains=patch, gameNumber__exact=draftPickOrder.gameNumner)
        
        pickPosition : int = getPickPosition(championName, draftPickOrder, side)
        enemyRoleList : list = getEnemyRoleList(draftPickOrder, queryPlayerPicks, side)
        
        
        role : str = getRoleForBlind(championName, queryPlayerPicks)
        if isBlind(pickPosition, role, enemyRoleList, side):
            counterBlinded += 1
        
    blindPickRate : float = counterBlinded/amountOfGames
    return blindPickRate

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
                   winRate : float,
                   pickRate : float,
                   pickRate1Rota : float,
                   pickRate2Rota : float,
                   banRate : float,
                   banRate1Rota : float,
                   banRate2Rota : float,
                   mostPopularPickOrder : int,
                   blindPick : float,
                   mostPopularRole : str) -> None:
    df : pd.DataFrame = pd.read_csv(path, sep=";")
    for index, row in df.iterrows():
        # Getting the line we want

        if row["ChampionName"] == championName and str(row["Patch"]) == patch and row["Tournament"] == tournament and row["Side"] == side:
            # If input data is different than csv data
            if not(abs(winRate - row["WinRate"]) < 0.01 
                   and abs(row["GlobalPickRate"] - pickRate) < 0.01
                   and abs(row["PickRate1Rota"] - pickRate1Rota) < 0.01
                   and abs(row["PickRate2Rota"] - pickRate2Rota) < 0.01
                   and abs(row["GlobalBanRate"] - banRate) < 0.01
                   and abs(row["BanRate1Rota"] - banRate1Rota) < 0.01
                   and abs(row["BanRate2Rota"] - banRate2Rota) < 0.01
                   and row["MostPopularPickOrder"] == mostPopularPickOrder
                   and abs(row["BlindPick"] - blindPick) < 0.01
                   and row["MostPopularRole"] == mostPopularRole):
                
                print("Updating row")
                df.at[index, "WinRate"] = winRate
                df.at[index, "GlobalPickRate"] = pickRate
                df.at[index, "PickRate1Rota"] = pickRate1Rota
                df.at[index, "PickRate2Rota"] = pickRate2Rota
                df.at[index, "GlobalBanRate"] = banRate
                df.at[index, "BanRate1Rota"] = banRate1Rota
                df.at[index, "BanRate2Rota"] = banRate2Rota
                df.at[index, "MostPopularPickOrder"] = mostPopularPickOrder
                df.at[index, "BlindPick"] = blindPick
                df.at[index, "MostPopularRole"] = mostPopularRole

                os.remove(path)
                df.to_csv(path, sep=";", index=False)
                break
            
            else:
                print("Row not modified")
                
def getMostPopularRole(championName : str, tournament : str, patch : str, side : str) -> float:
    queryDraftPickOrder = DraftPickOrder.objects.filter(tournament__exact=tournament, patch__contains=patch)

    roleCounterDict : dict = {
        "Top" : 0,
        "Jungle": 0,
        "Mid": 0,
        "ADC": 0,
        "Support": 0
    }

    for draftPickOrder in queryDraftPickOrder:
        bluePicks = [
            draftPickOrder.bp1,
            draftPickOrder.bp2,
            draftPickOrder.bp3,
            draftPickOrder.bp4,
            draftPickOrder.bp5
        ]
        redPicks = [
            draftPickOrder.rp1,
            draftPickOrder.rp2,
            draftPickOrder.rp3,
            draftPickOrder.rp4,
            draftPickOrder.rp5
        ]
        if championName in bluePicks and side == "Blue":
            queryPlayerPicks = DraftPlayerPick.objects.filter(seriesId__exact=draftPickOrder.seriesId, tournament__exact=tournament, patch__contains=patch, gameNumber__exact=draftPickOrder.gameNumner)

            role : str = getRoleForBlind(championName, queryPlayerPicks)
            roleCounterDict[role] += 1
        elif championName in redPicks and side == "Red":
            queryPlayerPicks = DraftPlayerPick.objects.filter(seriesId__exact=draftPickOrder.seriesId,tournament__exact=tournament, patch__contains=patch, gameNumber__exact=draftPickOrder.gameNumner)

            role : str = getRoleForBlind(championName, queryPlayerPicks)
            roleCounterDict[role] += 1

    mostPopularRole : str = "Top"
    max = roleCounterDict[mostPopularRole]
    for role, counter in roleCounterDict.items():
        if counter > max:
            mostPopularRole = role
    
    return mostPopularRole
 
def saveChampionDraftStatsCSV(path : str,
                              new : bool,
                              championName : str,
                              patch : str,
                              tournament : str,
                              side : str,
                              winRate : float,
                              pickRate : float,
                              pickRate1Rota : float,
                              pickRate2Rota : float,
                              banRate : float,
                              banRate1Rota : float,
                              banRate2Rota : float,
                              mostPopularPickOrder : int,
                              blindPick : float,
                              mostPopularRole : str) -> None:
    
    if new:
        write_option : str = "w"
    else:
        write_option : str = "a"

    
    
    csv_file = open(path, write_option)
    writer = csv.writer(csv_file, delimiter=";")
    if new:
        header = ["ChampionName", "Patch", "Tournament", "Side", "WinRate", "GlobalPickRate", "PickRate1Rota", "PickRate2Rota", "GlobalBanRate", "BanRate1Rota", "BanRate2Rota", "MostPopularPickOrder", "BlindPick", "MostPopularRole"]
        writer.writerow(header)
        data = [championName, patch, tournament, side, winRate, pickRate, pickRate1Rota, pickRate2Rota, banRate, banRate1Rota, banRate2Rota, mostPopularPickOrder, blindPick, mostPopularRole]

        writer.writerow(data)
        csv_file.close()
    elif isLineInDatabase(path, championName, patch, tournament, side):
        print(" Is In database")
        csv_file.close()
        updateDatabase(
            path,
            championName,
            patch,
            tournament,
            side,
            winRate,
            pickRate,
            pickRate1Rota,
            pickRate2Rota,
            banRate,
            banRate1Rota,
            banRate2Rota,
            mostPopularPickOrder,
            blindPick,
            mostPopularRole,
        )
    else:
        data = [championName, patch, tournament, side, winRate, pickRate, pickRate1Rota, pickRate2Rota, banRate, banRate1Rota, banRate2Rota, mostPopularPickOrder, blindPick, mostPopularRole]

        writer.writerow(data)
        csv_file.close()
    
        
    print(" Saving to database")

