from .globals import DATA_PATH, ROLE_LIST, DATE_LIMIT

from behaviorADC.models import *
from dataAnalysis.models import GameMetadata
from dataAnalysis.packages.api_calls.GRID.get_token import get_token
from dataAnalysis.packages.Parsers.Separated.Game.SeparatedData import SeparatedData

import pandas as pd
import re
import time
from datetime import datetime
import requests
import json

def isGameDownloaded(seriesId : int, gameNumber : int):
    df = pd.read_csv(DATA_PATH + "games/data_metadata.csv", sep=";")
    for _, row in df.iterrows():
        if row["SeriesId"] == seriesId and row["gameNumber"] == gameNumber:
            return True
    return False

def import_Behavior_ADC():
    csv_file_path = "./databases/behavior/behavior/behavior_ADC.csv"
    df = pd.read_csv(csv_file_path, sep=";")


    for index, row in df.iterrows():
        behaviorADC = BehaviorADC(
            date = row["Date"],
            tournament = row["Tournament"],
            matchId = row["MatchId"],
            summonnerName = row["SummonnerName"],
            patch = row["Patch"],
            seriesId = row["SeriesId"],
            xpd15 = row["XPD@15"],
            gd15 = row["GD@15"],
            csMin = row["CS/Min"],
            kills = row["Kills"],
            deaths = row["Deaths"],
            assists = row["Assists"],
            kp = row["KP%"],
            dpm = row["Damage/Min"],
            jungleProximity = row["JungleProximity"],
            botLanePresence = row["botLanePresence"],
            riverBotPresence = row["riverBotPresence"],
            gameNumber = row["GameNumber"]
        )

        if not(BehaviorADC.objects.filter(
            date = row["Date"],
            tournament = row["Tournament"],
            matchId = row["MatchId"],
            summonnerName = row["SummonnerName"],
            patch = row["Patch"],
            seriesId = row["SeriesId"],
            xpd15 = row["XPD@15"],
            gd15 = row["GD@15"],
            csMin = row["CS/Min"],
            kills = row["Kills"],
            deaths = row["Deaths"],
            assists = row["Assists"],
            kp = row["KP%"],
            dpm = row["Damage/Min"],
            jungleProximity = row["JungleProximity"],
            botLanePresence = row["botLanePresence"],
            riverBotPresence = row["riverBotPresence"],
            gameNumber = row["GameNumber"]
        ).count() > 0):
            behaviorADC.save()

    print("ADC Behavior imported")

def import_Behavior_Jungle():
    csv_file_path = "./databases/behavior/behavior/behavior_Jungle.csv"
    df = pd.read_csv(csv_file_path, sep=";")


    for index, row in df.iterrows():
        behaviorJungle = BehaviorJungle(
            date = row["Date"],
            tournament = row["Tournament"],
            matchId = row["MatchId"],
            summonnerName = row["SummonnerName"],
            patch = row["Patch"],
            seriesId = row["SeriesId"],
            xpd15 = row["XPD@15"],
            gd15 = row["GD@15"],
            kills = row["Kills"],
            deaths = row["Deaths"],
            assists = row["Assists"],
            kp = row["KP%"],
            dpm = row["Damage/Min"],
            topLanePresence = row["topLanePresence"],
            midLanePresence = row["midLanePresence"],
            botLanePresence = row["botLanePresence"],
            jungleAllyTopPresence = row["jungleAllyTopPresence"],
            jungleAllyBotPresence = row["jungleAllyBotPresence"],
            jungleEnemyTopPresence = row["jungleEnemyTopPresence"],
            jungleEnemyBotPresence = row["jungleEnemyBotPresence"],
            riverBotPresence = row["riverBotPresence"],
            riverTopPresence = row["riverTopPresence"],
            gameNumber = row["GameNumber"]
        )

        if not(BehaviorJungle.objects.filter(
            date = row["Date"],
            tournament = row["Tournament"],
            matchId = row["MatchId"],
            summonnerName = row["SummonnerName"],
            patch = row["Patch"],
            seriesId = row["SeriesId"],
            xpd15 = row["XPD@15"],
            gd15 = row["GD@15"],
            kills = row["Kills"],
            deaths = row["Deaths"],
            assists = row["Assists"],
            kp = row["KP%"],
            dpm = row["Damage/Min"],
            topLanePresence = row["topLanePresence"],
            midLanePresence = row["midLanePresence"],
            botLanePresence = row["botLanePresence"],
            jungleAllyTopPresence = row["jungleAllyTopPresence"],
            jungleAllyBotPresence = row["jungleAllyBotPresence"],
            jungleEnemyTopPresence = row["jungleEnemyTopPresence"],
            jungleEnemyBotPresence = row["jungleEnemyBotPresence"],
            riverBotPresence = row["riverBotPresence"],
            riverTopPresence = row["riverTopPresence"],
            gameNumber = row["GameNumber"]
        ).count() > 0):
            behaviorJungle.save()

    print("Jungle Behavior imported")

def import_Behavior_Mid():
    csv_file_path = "./databases/behavior/behavior/behavior_Mid.csv"
    df = pd.read_csv(csv_file_path, sep=";")


    for index, row in df.iterrows():
        behaviorMid = BehaviorMid(
            date = row["Date"],
            tournament = row["Tournament"],
            matchId = row["MatchId"],
            seriesId = row["SeriesId"],
            patch = row["Patch"],
            summonnerName = row["SummonnerName"],
            xpd15 = row["XPD@15"],
            gd15 = row["GD@15"],
            csMin = row["CS/Min"],
            kills = row["Kills"],
            deaths = row["Deaths"],
            assists = row["Assists"],
            kp = row["KP%"],
            wardPlaced = row["WardPlaced"],
            wardKilled = row["WardKilled"],
            dpm = row["Damage/Min"],
            totalDamageDealtToBuilding = row["TotalDamageDealtToBuilding"],
            totalDamageDealtToObjectives = row["TotalDamageDealtToObjectives"],
            jungleProximity = row["JungleProximity"],
            topLanePresence = row["topLanePresence"],
            midLanePresence = row["midLanePresence"],
            botLanePresence = row["botLanePresence"],
            jungleAllyTopPresence = row["jungleAllyTopPresence"],
            jungleAllyBotPresence = row["jungleAllyBotPresence"],
            jungleEnemyTopPresence = row["jungleEnemyTopPresence"],
            jungleEnemyBotPresence = row["jungleEnemyBotPresence"],
            riverBotPresence = row["riverBotPresence"],
            riverTopPresence = row["riverTopPresence"],
            gameNumber = row["GameNumber"],
        )

        if not(BehaviorMid.objects.filter(
           date = row["Date"],
            tournament = row["Tournament"],
            matchId = row["MatchId"],
            seriesId = row["SeriesId"],
            patch = row["Patch"],
            summonnerName = row["SummonnerName"],
            xpd15 = row["XPD@15"],
            gd15 = row["GD@15"],
            csMin = row["CS/Min"],
            kills = row["Kills"],
            deaths = row["Deaths"],
            assists = row["Assists"],
            kp = row["KP%"],
            wardPlaced = row["WardPlaced"],
            wardKilled = row["WardKilled"],
            dpm = row["Damage/Min"],
            totalDamageDealtToBuilding = row["TotalDamageDealtToBuilding"],
            totalDamageDealtToObjectives = row["TotalDamageDealtToObjectives"],
            jungleProximity = row["JungleProximity"],
            topLanePresence = row["topLanePresence"],
            midLanePresence = row["midLanePresence"],
            botLanePresence = row["botLanePresence"],
            jungleAllyTopPresence = row["jungleAllyTopPresence"],
            jungleAllyBotPresence = row["jungleAllyBotPresence"],
            jungleEnemyTopPresence = row["jungleEnemyTopPresence"],
            jungleEnemyBotPresence = row["jungleEnemyBotPresence"],
            riverBotPresence = row["riverBotPresence"],
            riverTopPresence = row["riverTopPresence"],
            gameNumber = row["GameNumber"], 
        ).count() > 0):

            behaviorMid.save()
    print("Mid Behavior imported")

def import_Behavior_Support():
    csv_file_path = "./databases/behavior/behavior/behavior_Support.csv"
    df = pd.read_csv(csv_file_path, sep=";")


    for index, row in df.iterrows():
        behaviorSupport = BehaviorSupport(
            date = row["Date"],
            tournament = row["Tournament"],
            matchId = row["MatchId"],
            seriesId = row["SeriesId"],
            patch = row["Patch"],
            summonnerName = row["SummonnerName"],
            xpd15 = row["XPD@15"],
            gd15 = row["GD@15"],
            deaths = row["Deaths"],
            kp = row["KP%"],
            wardPlaced = row["WardPlaced"],
            wardKilled = row["WardKilled"],
            dpm = row["Damage/Min"],
            jungleProximity = row["JungleProximity"],
            topLanePresence = row["topLanePresence"],
            midLanePresence = row["midLanePresence"],
            botLanePresence = row["botLanePresence"],
            jungleAllyTopPresence = row["jungleAllyTopPresence"],
            jungleAllyBotPresence = row["jungleAllyBotPresence"],
            jungleEnemyTopPresence = row["jungleEnemyTopPresence"],
            jungleEnemyBotPresence = row["jungleEnemyBotPresence"],
            riverBotPresence = row["riverBotPresence"],
            riverTopPresence = row["riverTopPresence"],
            gameNumber = row["GameNumber"]
        )

        if not(BehaviorSupport.objects.filter(
            date = row["Date"],
            tournament = row["Tournament"],
            matchId = row["MatchId"],
            seriesId = row["SeriesId"],
            patch = row["Patch"],
            summonnerName = row["SummonnerName"],
            xpd15 = row["XPD@15"],
            gd15 = row["GD@15"],
            deaths = row["Deaths"],
            kp = row["KP%"],
            wardPlaced = row["WardPlaced"],
            wardKilled = row["WardKilled"],
            dpm = row["Damage/Min"],
            jungleProximity = row["JungleProximity"],
            topLanePresence = row["topLanePresence"],
            midLanePresence = row["midLanePresence"],
            botLanePresence = row["botLanePresence"],
            jungleAllyTopPresence = row["jungleAllyTopPresence"],
            jungleAllyBotPresence = row["jungleAllyBotPresence"],
            jungleEnemyTopPresence = row["jungleEnemyTopPresence"],
            jungleEnemyBotPresence = row["jungleEnemyBotPresence"],
            riverBotPresence = row["riverBotPresence"],
            riverTopPresence = row["riverTopPresence"],
            gameNumber = row["GameNumber"]
        ).count() > 0):
            behaviorSupport.save()
    print("Support Behavior imported")

def import_Behavior_Top():
    csv_file_path = "./databases/behavior/behavior/behavior_Top.csv"
    df = pd.read_csv(csv_file_path, sep=";")


    for index, row in df.iterrows():
        behaviorTop = BehaviorTop(
            date = row["Date"],
            tournament = row["Tournament"],
            matchId = row["MatchId"],
            summonnerName = row["SummonnerName"],
            patch = row["Patch"],
            seriesId = row["SeriesId"],
            xpd15 = row["XPD@15"],
            gd15 = row["GD@15"],
            csMin = row["CS/Min"],
            kills = row["Kills"],
            deaths = row["Deaths"],
            assists = row["Assists"],
            kp = row["KP%"],
            wardPlaced = row["WardPlaced"],
            dpm = row["Damage/Min"],
            totalDamageDealtToBuilding = row["TotalDamageDealtToBuilding"],
            totalDamageDealtToObjectives = row["TotalDamageDealtToObjectives"],
            jungleProximity = row["JungleProximity"],
            topLanePresence = row["topLanePresence"],
            jungleAllyTopPresence = row["jungleAllyTopPresence"],
            jungleEnemyTopPresence = row["jungleEnemyTopPresence"],
            riverTopPresence = row["riverTopPresence"],
            gameNumber = row["GameNumber"]
        )

        if not(BehaviorTop.objects.filter(
            date = row["Date"],
            tournament = row["Tournament"],
            matchId = row["MatchId"],
            summonnerName = row["SummonnerName"],
            patch = row["Patch"],
            seriesId = row["SeriesId"],
            xpd15 = row["XPD@15"],
            gd15 = row["GD@15"],
            csMin = row["CS/Min"],
            kills = row["Kills"],
            deaths = row["Deaths"],
            assists = row["Assists"],
            kp = row["KP%"],
            wardPlaced = row["WardPlaced"],
            dpm = row["Damage/Min"],
            totalDamageDealtToBuilding = row["TotalDamageDealtToBuilding"],
            totalDamageDealtToObjectives = row["TotalDamageDealtToObjectives"],
            jungleProximity = row["JungleProximity"],
            topLanePresence = row["topLanePresence"],
            jungleAllyTopPresence = row["jungleAllyTopPresence"],
            jungleEnemyTopPresence = row["jungleEnemyTopPresence"],
            riverTopPresence = row["riverTopPresence"],
            gameNumber = row["GameNumber"]).count() > 0):

            behaviorTop.save()
    print("Top Behavior imported")

def import_Behavior():
    import_Behavior_Top()
    import_Behavior_Jungle()
    import_Behavior_Mid()
    import_Behavior_ADC()
    import_Behavior_Support()


def convertDate(date : str):
    return re.sub(r"T[0-9]+:[0-9]+:[0-9]+Z", "", date)

# T[0-9]+:[0-9]+:[0-9]+Z

def isDateValid(date:str):
    date_limit = datetime.strptime(DATE_LIMIT, "%Y-%m-%d")
    date_to_compare = datetime.strptime(date, "%Y-%m-%d")
    return date_to_compare > date_limit

def checkFiles(fileList : list[dict]) -> bool:
    i = 0
    firstFile = fileList[i]
    grid_summary_regex = re.search(r"Grid Post Series State", firstFile["description"])
    flag_grid_summary : bool = grid_summary_regex != None
    while not(flag_grid_summary) and i < len(fileList):
        i += 1
        grid_summary_regex = re.search(r"Grid Post Series State", fileList[i]["description"])
        flag_grid_summary : bool = grid_summary_regex != None
    j = 0
    firstFile = fileList[j]
    riot_livestats_regex = re.search(r"Riot LiveStats", firstFile["description"])
    flag_riot_livestats : bool = riot_livestats_regex != None
    while not(flag_riot_livestats) and j < len(fileList):
        j += 1
        riot_livestats_regex = re.search(r"Riot LiveStats", fileList[j]["description"])
        flag_riot_livestats : bool = riot_livestats_regex != None

    return i < len(fileList) and j < len(fileList)

def checkSeries(fileList : list[dict]) -> bool:
    time.sleep(1)
    for file in fileList:
        x = re.search(r"Riot LiveStats", file["description"])
        if x != None:
            url : str = file["fullURL"]
            token = get_token()
            headers = {
                "x-api-key": token
            }
            response = requests.get(url=url, headers=headers)
            if response.status_code != 200:
                response.raise_for_status()

            live_data = response.content.decode('utf-8').splitlines()
            if len(live_data) < 500:
                return False
            
    return True

def getNbGamesSeries(fileList : list[dict]) -> int:
    cpt = 0
    for file in fileList:
        x = re.search(r"Riot LiveStats", file["description"])
        if x != None:
            cpt += 1
    return cpt

def getPlayerSide(data : SeparatedData, seriesId : int, gameNumber : int, sumonnerName : str):
    # Get the player side
    # Getting the corresponding team index of our player
    teamIdx : int = -1
    if data.gameSnapshotList[0].teams[0].getPlayerID(sumonnerName) == -1 :
        teamIdx = 1
    else:
        teamIdx = 0
    teamName = data.gameSnapshotList[0].teams[teamIdx].getTeamName(seriesId)
    # Get the game metadata we want
    side : str = ""
    gameMetada = GameMetadata.objects.get(seriesId__exact=seriesId, gameNumber__exact=gameNumber)
    if gameMetada.teamBlue == teamName:
        side = "Blue"
    else:
        side = "Red"
    return side

def getPlayerTeam(data : SeparatedData, sumonnerName : str, seriesId : int):
    teamIdx : int = -1
    if data.gameSnapshotList[0].teams[0].getPlayerID(sumonnerName) == -1 :
        teamIdx = 1
    else:
        teamIdx = 0
    teamName = data.gameSnapshotList[0].teams[teamIdx].getTeamName(seriesId)
    return teamName
