from ..models import ChampionPool, DraftPlayerPick, DraftPickOrder
from dataAnalysis.models import GameMetadata
from dataAnalysis.packages.utils_stuff.utils_func import getData
from dataAnalysis.packages.Parsers.Separated.Game.Player import Player
from dataAnalysis.globals import DATE_LIMIT

import csv
import pandas as pd
import os
from datetime import datetime

def isPlayerChampionStatInDatabase(playerName, championName, tournament):
    return ChampionPool.objects.filter(
        summonnerName__exact=playerName, 
        championName__exact=championName, 
        tournament__exact=tournament
    ).count() > 0

def getPlayerChampionPickRate(playerName : str, championName : str,  tournament : str) -> float:
    if tournament == "League of Legends Scrim":
        pickCounter : int = DraftPlayerPick.objects.filter(sumonnerName__exact=playerName, tournament__exact=tournament, championName__exact=championName, date__gte=DATE_LIMIT).count()
        totalGames : int = DraftPlayerPick.objects.filter(sumonnerName__exact=playerName, tournament__exact=tournament, date__gte=DATE_LIMIT).count()
    else:
        pickCounter : int = DraftPlayerPick.objects.filter(sumonnerName__exact=playerName, tournament__exact=tournament, championName__exact=championName).count()
        totalGames : int = DraftPlayerPick.objects.filter(sumonnerName__exact=playerName, tournament__exact=tournament).count()
    return pickCounter/totalGames

def getPlayerChampionWinRate(playerName : str, championName : str, tournament : str) -> float:
    if tournament == "League of Legends Scrim":
        queryGames = DraftPlayerPick.objects.filter(sumonnerName__exact=playerName, championName__exact=championName, tournament__exact=tournament, date__gte=DATE_LIMIT)
    else:
        queryGames = DraftPlayerPick.objects.filter(sumonnerName__exact=playerName, championName__exact=championName, tournament__exact=tournament)
    winCounter : int = 0
    totalGames : int = len(queryGames)
    
    # Getting the list of (seriesId, gameNumber) where the player picked the champion
    gameList : list[tuple] = list()
    for res in queryGames:
        gameList.append((res.seriesId, res.gameNumber))

    # Incrementing the winCounter everytime the player was in the winning team
    for (seriesId, gameNumber) in gameList:
        draftPickOrder = DraftPickOrder.objects.get(gameNumner__exact=gameNumber, seriesId__exact=seriesId)
        
        teamNamePlayer = playerName.split(" ")[0]

        if teamNamePlayer == draftPickOrder.teamBlue and draftPickOrder.winner == 0:
            winCounter += 1
        elif teamNamePlayer == draftPickOrder.teamRed and draftPickOrder.winner == 1:
            winCounter += 1
        
    return winCounter/totalGames

def getPlayerChampionNbGames(playerName : str, championName : str, tournament : str) -> int:
    if tournament == "League of Legends Scrims":
        return DraftPlayerPick.objects.filter(sumonnerName__exact=playerName, championName__exact=championName, tournament__exact=tournament, date__gte=DATE_LIMIT).count()
    else:
        return DraftPlayerPick.objects.filter(sumonnerName__exact=playerName, championName__exact=championName, tournament__exact=tournament).count()

def getPlayerChampionKDA(playerName : str, championName : str, tournament : str) -> float:
    if tournament == "League of Legends Scrims":
        queryGames = DraftPlayerPick.objects.filter(sumonnerName__exact=playerName, championName__exact=championName, tournament__exact=tournament, date__gte=DATE_LIMIT)
    else:
        queryGames = DraftPlayerPick.objects.filter(sumonnerName__exact=playerName, championName__exact=championName, tournament__exact=tournament)

    sumKDA : float = 0.0
    totalGames = len(queryGames)

    # Getting the list of (seriesId, gameNumber) where the player picked the champion
    gameList : list[tuple] = list()
    for res in queryGames:
        gameList.append((res.seriesId, res.gameNumber))

    for (seriesId, gameNumber) in gameList:
        (data, _, _, _) = getData(seriesId, gameNumber)

        if data.gameSnapshotList[-1].teams[0].getPlayerID(playerName) != -1:
            participantID = data.gameSnapshotList[-1].teams[0].getPlayerID(playerName)
            participantIdx = data.gameSnapshotList[-1].teams[0].getPlayerIdx(participantID)
            player : Player = data.gameSnapshotList[-1].teams[0].players[participantIdx]
            
            if player.stats.numDeaths == 0:
                kda = player.stats.championsKilled + player.stats.assists
            else:
                kda = (player.stats.championsKilled + player.stats.assists)/player.stats.numDeaths
            
            sumKDA += kda
        elif data.gameSnapshotList[-1].teams[1].getPlayerID(playerName) != -1:
            participantID = data.gameSnapshotList[-1].teams[1].getPlayerID(playerName)
            participantIdx = data.gameSnapshotList[-1].teams[1].getPlayerIdx(participantID)
            player : Player = data.gameSnapshotList[-1].teams[1].players[participantIdx]
            
            if player.stats.numDeaths == 0:
                kda = player.stats.championsKilled + player.stats.assists
            else:
                kda = (player.stats.championsKilled + player.stats.assists)/player.stats.numDeaths
            
            sumKDA += kda
        
    return sumKDA/totalGames

def isLineInDatabase(path : str, playerName : str, championName : str, tournament : str) -> bool:
    df : pd.DataFrame = pd.read_csv(path, sep=";")

    if df.empty:
        return False
    else:
        for _, row in df.iterrows():
            if row["SummonnerName"] == playerName and row["ChampionName"] == championName and row["Tournament"] == tournament:
                return True

        return False

def updateDatabase(path : str,
                   playerName : str, 
                   championName : str, 
                   tournament : str,
                   globalPickRate : float,
                   globalWinRate : float,
                   nbGames : int,
                   kda : float):
    df : pd.DataFrame = pd.read_csv(path, sep=";")
    for index, row in df.iterrows():
        # Getting the line we want

        if row["SummonnerName"] == playerName and row["ChampionName"] == championName and row["Tournament"] == tournament:
            # If input data is difference than csv data
            if not(abs(globalPickRate - row["GlobalPickRate"]) < 0.01
                   and abs(globalWinRate - row["WinRate"]) < 0.01
                   and abs(kda - row["KDA"] < 0.01)
                   and row["NbGames"] == nbGames):
                
                print("Updating row")
                df.at[index, "GlobalPickRate"] = globalPickRate
                df.at[index, "WinRate"] = globalWinRate
                df.at[index, "KDA"] = kda
                df.at[index, "NbGames"] = nbGames
                
                os.remove(path)
                df.to_csv(path, sep=";", index=False)
                break

def saveChampionPoolCSV(path : str,
                        new : bool,
                        playerName : str, 
                        championName : str, 
                        tournament : str,
                        globalPickRate : float,
                        globalWinRate : float,
                        nbGames : int,
                        kda : float) -> None:
    
    if new:
        write_option : str = "w"
    else:
        write_option : str = "a"

    csv_file = open(path, write_option)
    writer = csv.writer(csv_file, delimiter=";")
    if new:
        header = ["SummonnerName", "ChampionName", "Tournament", "GlobalPickRate", "WinRate", "NbGames", "KDA"]
        writer.writerow(header)
        data = [playerName, championName, tournament, globalPickRate, globalWinRate, nbGames, kda]
        
        writer.writerow(data)
        csv_file.close()
    
    elif isLineInDatabase(path, playerName, championName, tournament):
        csv_file.close()
        updateDatabase(
            path,
            playerName,
            championName,
            tournament,
            globalPickRate,
            globalWinRate,
            nbGames,
            kda,
        )
    else:
        data = [playerName, championName, tournament, globalPickRate, globalWinRate, nbGames, kda]

        writer.writerow(data)
        csv_file.close()
