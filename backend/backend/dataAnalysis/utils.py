from .globals import DATA_PATH, ROLE_LIST, DATE_LIMIT

from behaviorADC.models import *
from dataAnalysis.packages.api_calls.GRID.get_token import get_token

import pandas as pd
import re
import time
from datetime import datetime
import requests

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