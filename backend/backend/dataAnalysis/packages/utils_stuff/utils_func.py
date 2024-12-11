import json
import pandas as pd
import os
import re
import pickle
import shutil
import csv
import time as t_time

from dataAnalysis.packages.utils_stuff.globals import *
from dataAnalysis.packages.Parsers.EMH.Summary.SummaryData import SummaryData
from dataAnalysis.globals import DATA_PATH

from dataAnalysis.packages.Parsers.Separated.Game.SeparatedData import SeparatedData
from dataAnalysis.packages.api_calls.GRID.api_calls import get_date_from_seriesId, get_tournament_from_seriesId
from dataAnalysis.utils import isGameDownloaded, convertDate

def get_all_event_types(json_path_details:str) -> dict:
    with open(json_path_details, 'r') as f:
        data = json.loads(f.read())
    df = pd.json_normalize(data)
    frames = df['frames'][0]
    
    unique_event_type : dict = dict()
    for frame in frames: # Looping throug every frame snapshot
        events = frame['events']
        for event in events: # Looping throug every event of that snapshot
            event_attributes = list(event.keys())
            if not(event['type'] in list(unique_event_type.keys())):
                unique_event_type[event['type']] = event_attributes
        
    
    for (_, v) in unique_event_type.items():
        v.remove('type')
    
    return unique_event_type


def getGameDuration(seriesId : int, gameNumber : int):
    match : str = "{}_ESPORTS_{}".format(seriesId, gameNumber)
    rootdir = DATA_PATH + "games/bin/{}".format(match)

    flagNew = False
    flagOld = False

    for _, _, files in os.walk(rootdir):
        for file in files:
            x = re.search(r"end_state_" + str(seriesId) + r"_grid.json", file)
            y = re.search(r"end_state_summary_riot_" + str(seriesId) + r"_" + str(gameNumber) + ".json", file)
            if x != None:
                flagNew = True
            elif y != None:
                flagOld = True  
    
    if flagNew:
        path = rootdir + "/end_state_" + str(seriesId) + "_grid.json"
        with open(path, "r") as json_file:
            res : dict = json.load(json_file)
            return res["games"][gameNumber-1]["clock"]["currentSeconds"]
    if flagOld:
        path = rootdir + "/end_state_summary_riot_" + str(seriesId) + "_" + str(gameNumber) + ".json"
        with open(path, "r") as json_file:
            res : dict = json.load(json_file)
            return res["gameDuration"]

def getSummaryData(seriesId : int, gameNumber : int) -> SummaryData:
    match : str = "{}_ESPORTS_{}".format(seriesId, gameNumber)

    pathSummaryData : str = DATA_PATH + "games/bin" + match + "end_state_summary_riot_" + seriesId + "_" + gameNumber + ".json"
    summaryData : SummaryData = SummaryData(pathSummaryData)
    return summaryData

def getData(seriesId : int, gameNumber : int):
    
    match : str = "{}_ESPORTS_{}".format(seriesId, gameNumber)

    rootdir = DATA_PATH + "games/bin/{}".format(match)

    pathData = DATA_PATH + "games/bin/" + match + "dataSeparatedRIOT"
    data : SeparatedData = None

    if not(os.path.exists(pathData)):
        data = SeparatedData(rootdir + "/Separated")
        pathData = DATA_PATH + "games/bin/" + match + "dataSeparatedRIOT"
        file = open(pathData, 'ab')
        pickle.dump(data, file)
        if os.path.exists(DATA_PATH + "games/bin/" + match + "/Separated/"):
            shutil.rmtree(DATA_PATH + "games/bin/" + match + "/Separated/")

        file.close()

        if not(isGameDownloaded(seriesId, gameNumber)):
            with open(DATA_PATH + "games/data_metadata.csv", "a") as csv_file:
                writer = csv.writer(csv_file, delimiter=";")
                matchDate = convertDate(get_date_from_seriesId(seriesId))
                matchName = match + "dataSeparatedRIOT"
                patch = data.patch
                teamBlue = data.gameSnapshotList[0].teams[0].getTeamName(seriesId)
                t_time.sleep(1)
                teamRed = data.gameSnapshotList[0].teams[1].getTeamName(seriesId)
                t_time.sleep(1)
                winningTeam = data.winningTeam
                tournament = get_tournament_from_seriesId(seriesId)
                summaryData : SummaryData = getSummaryData(seriesId, gameNumber)
                dragonBlueKills : int = summaryData.getObjectiveCount(0, "dragon")
                dragonRedKills : int = summaryData.getObjectiveCount(1, "dragon")
                krubsBlueKills : int = summaryData.getObjectiveCount(0, "horde")
                krubsRedKills : int = summaryData.getObjectiveCount(1, "horde")
                dataCSV = [
                    matchDate, 
                    tournament, 
                    matchName, 
                    patch, 
                    int(seriesId), 
                    teamBlue, 
                    teamRed, 
                    winningTeam, 
                    gameNumber, 
                    dragonBlueKills, 
                    dragonRedKills,
                    krubsBlueKills,
                    krubsRedKills
                ]
                
                writer.writerow(dataCSV)
    else:
        if os.path.exists(DATA_PATH + "games/bin/" + match + "/Separated/"):
            shutil.rmtree(DATA_PATH + "games/bin/" + match + "/Separated/")

        file = open(pathData, 'rb')
        data : SeparatedData = pickle.load(file)
        file.close()

    gameDuration : int = getGameDuration(seriesId, gameNumber)

    begGameTime : int = data.begGameTime
    endGameTime : int = data.endGameTime

    return (data, gameDuration, begGameTime, endGameTime)


def getUnsavedGameNames(gameNames : list[str], path : str) -> list[str]:
    res = []
    presentGameNames = []
    for root, _, _ in os.walk(path, topdown=False):
        presentGameNames.append(root.split("/")[2])

    for gameName in gameNames:
        if not(gameName in presentGameNames):
            res.append(gameName)
    return res
    
def getRole(data : SeparatedData, summonnerName : str = None, participantID : int = None):
    if summonnerName != None:
        participantID = data.getPlayerID(summonnerName)
    
    if data.gameSnapshotList[0].teams[0].isPlayerInTeam(participantID):
        participantIdx = data.gameSnapshotList[0].teams[0].getPlayerIdx(participantID)
        return roleMap[participantIdx]
    elif data.gameSnapshotList[0].teams[1].isPlayerInTeam(participantID):
        participantIdx = data.gameSnapshotList[0].teams[1].getPlayerIdx(participantID)
        return roleMap[participantIdx]
    
def splitPlayerNameListPerTeam(data : SeparatedData, playerNameList : list[str]):
    playerNameListTeamOne : list = list()
    playerNameListTeamTwo : list = list()

    for playerName in playerNameList:
        playerID = data.getPlayerID(playerName)
        if data.gameSnapshotList[0].teams[0].isPlayerInTeam(playerID):
            playerNameListTeamOne.append(playerName)
        elif data.gameSnapshotList[0].teams[1].isPlayerInTeam(playerID):
            playerNameListTeamTwo.append(playerName)
    return [playerNameListTeamOne, playerNameListTeamTwo]

def isInDataBase(matchId : str, date : str, role : str, summonnerName : str):
    res : bool = False

        
    save_path = DATA_PATH + "behavior/behavior/"
    full_path = save_path + "behavior_{}.csv".format(role)

    df : pd.DataFrame = pd.read_csv(full_path, delimiter=";")

    res = res or ((df["Date"] == date) & (df["MatchId"] == matchId) & df["SummonnerName"] == summonnerName).any()

    return res

def splitPlayerNameListPerTeam(data : SeparatedData, playerNameList : list[str]):
    playerNameListTeamOne : list = list()
    playerNameListTeamTwo : list = list()

    for playerName in playerNameList:
        playerID = data.getPlayerID(playerName)
        if data.gameSnapshotList[0].teams[0].isPlayerInTeam(playerID):
            playerNameListTeamOne.append(playerName)
        elif data.gameSnapshotList[0].teams[1].isPlayerInTeam(playerID):
            playerNameListTeamTwo.append(playerName)
    return [playerNameListTeamOne, playerNameListTeamTwo]
