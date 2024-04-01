import json
import pandas as pd
import os
import re
import pickle
import shutil
import csv

from dataAnalysis.packages.utils_stuff.globals import *
from dataAnalysis.packages.Parsers.EMH.Summary.SummaryData import SummaryData
from dataAnalysis.globals import DATA_PATH

from dataAnalysis.packages.Parsers.Separated.Game.SeparatedData import SeparatedData
from dataAnalysis.packages.api_calls.GRID.api_calls import get_date_from_seriesId
from dataAnalysis.utils import isGameDownloaded

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
        
def getSummaryData(rootdir : str) -> SummaryData:
    for subdir, _, files in os.walk(rootdir):
        for file in files:
            x = re.search("end_state_summary_riot", file)
            if x != None:
                return SummaryData(os.path.join(subdir, file))


def getData(seriesId : int, gameNumber : int):
    
    match : str = "{}_ESPORTS_{}".format(seriesId, gameNumber)

    rootdir = DATA_PATH + "games/bin/{}".format(match)
    summaryData = getSummaryData(rootdir)

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


        if not(isGameDownloaded(seriesId)):
            with open(DATA_PATH + "games/data_metadata.csv", "a") as csv_file:
                writer = csv.writer(csv_file, delimiter=";")
                matchDate = get_date_from_seriesId(seriesId)
                matchName = match + "dataSeparatedRIOT"
                patch = summaryData.patch
                teamBlue = data.gameSnapshotList[0].teams[0].getTeamName()
                teamRed = data.gameSnapshotList[0].teams[1].getTeamName()
                winningTeam = data.winningTeam
                dataCSV = [matchDate, matchName, patch, int(seriesId), teamBlue, teamRed, winningTeam]
                writer.writerow(dataCSV)
    else:
        if os.path.exists(DATA_PATH + "games/bin/" + match + "/Separated/"):
            shutil.rmtree(DATA_PATH + "games/bin/" + match + "/Separated/")

        file = open(pathData, 'rb')
        data : SeparatedData = pickle.load(file)
        file.close()

    if summaryData != None:
        gameDuration : int = summaryData.gameDuration
    else:
        gameDuration : int = -1
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