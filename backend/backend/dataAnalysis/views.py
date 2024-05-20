from django.shortcuts import render

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from behaviorADC.models import BehaviorTop, BehaviorJungle, BehaviorMid, BehaviorADC, BehaviorSupport
from .serializer import GameMetadataSerializer

from .globals import DATA_PATH, BLACKLIST, API_URL, ROLE_LIST
from .packages.api_calls.GRID.api_calls import *
from .utils import isGameDownloaded, import_Behavior, convertDate, isDateValid, checkSeries
from .packages.utils_stuff.utils_func import getData, getRole
from .packages.utils_stuff.stats import getProxomityMatrix
from .packages.Parsers.Separated.Game.SeparatedData import SeparatedData
from .packages.AreaMapping.AreaMapping import AreaMapping
from .packages.GameStat import GameStat
from .packages.BehaviorAnalysisRunner.behaviorAnalysis import getBehaviorData, saveToDataBase
from .packages.runners.pathing_runners import makeDensityPlot, getDataPathing
from .packages.Parsers.Separated.Game.Snapshot import Snapshot
from .packages.Parsers.Separated.Game.Team import Team


from Draft.models import DraftPlayerPick


from .models import GameMetadata

import json
import pandas as pd
from datetime import datetime
import re
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np


@api_view(['DELETE'])
def deleteGame(request, seriesId : int, gameNumber : int):
    wantedGame = GameMetadata.objects.filter(seriesId=seriesId, gameNumber=gameNumber)
    for res in wantedGame:
        res.delete()
    return Response(status=status.HTTP_200_OK)

@api_view(['PATCH'])
def download_latest(request, rawTournamentList : str):
    wantedTournamentList : list = rawTournamentList.split(",")
    
    # Getting the list of tournament in our database
    tournamentList : list = list()
    queryTournamentList = BehaviorADC.objects.all()
    for res in queryTournamentList:
        tournamentList.append(res.tournament)
    df = pd.DataFrame({'tournaments': tournamentList})
    tournamentList = df['tournaments'].unique().tolist()
    
    # Opening our tournament mapping json
    tournamentMapping : dict = None
    with open(DATA_PATH + "tournament_mapping.json", "r") as json_file:
        tournamentMapping = json.loads(json_file.read())


    # Mapping our wanted tournament to get the list of wanted ids
    wantedTournamentMapping : dict = dict()
    for wantedTournamentName in wantedTournamentList:
        for tournament_name, tournament_id  in tournamentMapping.items():
            if wantedTournamentName == tournament_name:
                wantedTournamentMapping[tournament_name] = tournament_id
    
    
    for tournament_name, tournament_id in wantedTournamentMapping.items():
        print(tournament_id, tournament_name)
        if tournament_name == "League of Legends Scrims":
            seriesIdList = get_all_game_seriesId_scrims(200, DATE_LIMIT)
        seriesIdList = get_all_game_seriesId_tournament(tournament_id, 200)
        
        
        for seriesId in seriesIdList:
        # for seriesId in seriesIdList:
            if not(seriesId in BLACKLIST):
                dlDict : dict = get_all_download_links(seriesId)
                i = 0
                if checkSeries(dlDict['files']):
                    print("\tChecking games of seriesId :", seriesId)
                    for downloadDict in dlDict['files']:
                        fileType = downloadDict["fileName"].split(".")[-1]
                        fileName = downloadDict["fileName"].split(".")[0]
                        
                        if i > 1 :
                            gameNumber = int(downloadDict["id"].split("-")[-1])

                        if fileType != "rofl" and downloadDict["status"] == "ready":
                            if i > 1:
                                # The first 2 files are global info about the Best-of
                                # We have 3 files per games
                                # We add 1 to start the gameNumber at 1
                                # gameNumber = (i-2)//3 + 1
                                date = convertDate(get_date_from_seriesId(seriesId))
                                flag = True
                                if tournament_name == "League of Legends Scrims":
                                    flag = isDateValid(date)
                                
                                if not(isGameDownloaded(int(seriesId), gameNumber)) and gameNumber < get_nb_games_seriesId(seriesId) + 1 and flag:

                                    path : str = DATA_PATH + "games/bin/" + "{}_{}_{}/".format(seriesId, "ESPORTS", gameNumber)
                                    print("\t\tDownloading {} files {}".format(fileName, gameNumber))
                                    download_from_link(downloadDict['fullURL'], fileName, path, fileType)

                            else:
                                for gameNumber in range(1, get_nb_games_seriesId(seriesId) + 1):
                                    if not(isGameDownloaded(int(seriesId), gameNumber)):
                                        path : str = DATA_PATH + "games/bin/" + "{}_{}_{}/".format(seriesId, "ESPORTS", gameNumber)
                                        print("\t\tDownloading {} info".format(fileName))
                                        download_from_link(downloadDict['fullURL'], fileName, path, fileType)
                        elif fileType == "rofl":
                            print("\t\twe don't download rofl file")
                        i += 1

                    # Save game metadata in csv and sqlite databases
                    print("Saving to database ({} games)".format(get_nb_games_seriesId(seriesId)))
                    for gameNumberIt in range(1, get_nb_games_seriesId(seriesId) + 1):
                        date = convertDate(get_date_from_seriesId(seriesId))
                        flag = True
                        if tournament_name == "League of Legends Scrims":
                            flag = isDateValid(date)
                        
                        if not(isGameDownloaded(int(seriesId), gameNumberIt)) and flag:
                            # print("saving to db")
                            # Getting relative information about the game
                            date = convertDate(get_date_from_seriesId(seriesId))
                            name : str = "{}_ESPORTS_{}dataSeparatedRIOT".format(seriesId, gameNumberIt)
                            (data, _, _, _) = getData(int(seriesId), gameNumberIt)
                            patch : str = data.patch
                            teamBlue : str = data.gameSnapshotList[0].teams[0].getTeamName(seriesId)
                            teamRed : str = data.gameSnapshotList[0].teams[1].getTeamName(seriesId)
                            winningTeam : int = data.winningTeam
                            tournament : str = get_tournament_from_seriesId(seriesId)
                            
                            # Saving game metadata to SQLite datbase
                            gameMetadata : GameMetadata = GameMetadata(date=date, tournament=tournament, name=name, patch=patch, seriesId=seriesId, teamBlue=teamBlue, teamRed=teamRed, winningTeam=winningTeam, gameNumber=gameNumberIt)
                            gameMetadata.save()
                        else :
                            print("game already downloaded")
    
    return Response(wantedTournamentMapping)

@api_view(['GET'])
def get_tournament_mapping(request):

    tournament_mapping : dict = get_all_tournament_ids("")
    if os.path.exists(DATA_PATH + "tournament_mapping.json"):
        os.remove(DATA_PATH + "tournament_mapping.json")
    
    with open(DATA_PATH + "tournament_mapping.json", "w") as json_file:
        json.dump(tournament_mapping, json_file)
    
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def get_tournament_list_shortened(request):
    tournament_list = []
    if os.path.exists(DATA_PATH + "tournament_list.json"):
        os.remove(DATA_PATH + "tournament_list.json")
    
    with open(DATA_PATH + "tournament_mapping.json") as json_file:
        tournament_mapping : dict = json.load(json_file)

        for tournament_name, _ in tournament_mapping.items():
            today_year = datetime.today().year
            x = re.search(r"- .*(" + str(today_year) + r"|" + str(today_year-1) + r") \(.+\)", tournament_name)
            
            if x != None :
                temp_name : str = tournament_name.split("-")[0][:-1]
                if not(temp_name in tournament_list):
                    tournament_list.append(temp_name)
    tournament_list.append("League of Legends Scrims")
    return Response(tournament_list)

@api_view(['GET'])
def get_patch_list(request):
    queryResult = GameMetadata.objects.all()
    patchList : list = list()

    for res in queryResult:
        patch = res.patch.split(".")[0] + "." + res.patch.split(".")[1]
        patchList.append(patch)
    df = pd.DataFrame({"patch": patchList})

    return Response(df["patch"].unique())

@api_view(['GET'])
def get_tournament_list(request):
    queryResult = DraftPlayerPick.objects.all()
    tournamentList : list = list()

    for res in queryResult:
        tournamentList.append(res.tournament)
    df = pd.DataFrame({'tournaments': tournamentList})
    return Response(df['tournaments'].unique())

@api_view(['PATCH'])
def update_bins(request):
    df = pd.read_csv(DATA_PATH + "games/data_metadata.csv",sep=";")

    for seriesId in df["SeriesId"].unique().tolist():
        gameNumber = 1
        if not(seriesId in BLACKLIST) and not(os.path.exists(DATA_PATH + "games/bin/{}_ESPORTS_1dataSeparatedRIOT".format(seriesId))):
            dlDict : dict = get_all_download_links(seriesId)
            print("\tChecking game of seriesId :", seriesId)
            i = 0
            for downloadDict in dlDict['files']:
                fileType = downloadDict["fileName"].split(".")[-1]
                fileName = downloadDict["fileName"].split(".")[0]

                if fileType != "rofl" and downloadDict["status"] == "ready":
                    if i > 1:
                        # The first 2 files are global info about the Best-of
                        # We have 4 files per games
                        # We add 1 to start the gameNumber list at 1
                        gameNumber = (i-2)//4 + 1
                        if gameNumber < get_nb_games_seriesId(seriesId) + 1:
                            path : str = DATA_PATH + "games/bin/" + "{}_{}_{}/".format(seriesId, "ESPORTS", gameNumber)
                            print("\t\tDownloading {} files".format(fileName))
                            download_from_link(downloadDict['fullURL'], fileName, path, fileType)

                elif fileType == "rofl":
                    print("\t\twe don't download rofl file")
                i += 1

            # Save game metadata in csv and sqlite databases
            print("Saving to database ({} games)".format(get_nb_games_seriesId(seriesId)))
            for gameNumberIt in range(1, get_nb_games_seriesId(seriesId) + 1):
                # Getting relative information about the game
                date = get_date_from_seriesId(seriesId)
                name : str = "{}_ESPORTS_{}dataSeparatedRIOT".format(seriesId, gameNumberIt)

                (data, _, _, _) = getData(int(seriesId), gameNumberIt)
                patch : str = data.patch
                teamBlue : str = data.gameSnapshotList[0].teams[0].getTeamName()
                teamRed : str = data.gameSnapshotList[1].teams[0].getTeamName()
                winningTeam : int = data.winningTeam

                
                # Saving game metadata to SQLite datbase
                gameMetadata : GameMetadata = GameMetadata(date=date, name=name, patch=patch, seriesId=seriesId, teamBlue=teamBlue, teamRed=teamRed, winningTeam=winningTeam, gameNumber=gameNumber)
                gameMetadata.save()

    return Response(status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_all_gameMetadata(request):
    query = GameMetadata.objects.all()
    for res in query:
        res.delete()

    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def getPatchListFromTournament(request, tournament):
    queryTournamentList = DraftPlayerPick.objects.all()
    tournamentList : list = list()

    for res in queryTournamentList:
        if not(res.tournament in tournamentList):
            tournamentList.append(res.tournament)

    if not(tournament in tournamentList):
        return Response(status=status.HTTP_400_BAD_REQUEST)


    queryPatchList = DraftPlayerPick.objects.filter(tournament__exact=tournament)
    patchList : list = list()
    for res in queryPatchList:
        tempPatch = res.patch.split(".")[0] + "." + res.patch.split(".")[1]
        if not(tempPatch in patchList):
            patchList.append(tempPatch)
    
    return Response(patchList)

@api_view(['GET'])
def getTournamentFromPlayer(request, summonnerName, patch):
    query = DraftPlayerPick.objects.filter(sumonnerName__exact=summonnerName, patch__contains=patch)
    print(len(query))
    tournamentList : list = list()
    for res in query:
        if not(res.tournament in tournamentList):
            tournamentList.append(res.tournament)

    return Response(tournamentList)

@api_view(['DELETE'])
def deleteAllBehaviorStats(request):
    queryTop = BehaviorTop.objects.all()
    for behaviorTop in queryTop:
        behaviorTop.delete()
    print("Deleted data from Top")

    queryJungle = BehaviorJungle.objects.all()
    for behaviorJungle in queryJungle:
        behaviorJungle.delete()
    print("Deleted data from Jungle")

    queryMid = BehaviorMid.objects.all()
    for behaviorMid in queryMid:
        behaviorMid.delete()
    print("Deleted data from Mid")

    queryADC = BehaviorADC.objects.all()
    for behaviorADC in queryADC:
        behaviorADC.delete()
    print("Deleted data from ADC")

    querySupport = BehaviorSupport.objects.all()
    for behaviorSupport in querySupport:
        behaviorSupport.delete()
    print("Deleted data from Support")

    return Response(status=status.HTTP_200_OK)

@api_view(['PATCH'])
def computeNewBehaviorStats(request, time):
    queryAllGames = GameMetadata.objects.all()

    for game in tqdm(queryAllGames):
    # for game in queryAllGames:
        if not(BehaviorADC.objects.filter(date=game.date, seriesId=game.seriesId, gameNumber=game.gameNumber).count() > 0):
            seriesId : int = game.seriesId
            gameNumber : int = game.gameNumber
            (data, gameDuration, begGameTime, endGameTime) = getData(seriesId, gameNumber)

            date = game.date
            matchId = data.matchId

            # usually time = 840s i.e 14min
            # Splitting our data so we get the interval between [840s; gameDuration]
            splitList : list[int] = [120, time, gameDuration]
            splittedDataset : list[SeparatedData] = data.splitData(gameDuration, splitList)
            areaMapping : AreaMapping = AreaMapping()

            dataBeforeTime : SeparatedData = splittedDataset[1] # Getting the wanted interval
            areaMapping.computeMapping(dataBeforeTime)
            tournamentName : str = get_tournament_from_seriesId(seriesId)


            # Getting game patch
            match : str = "{}_ESPORTS_{}".format(seriesId, gameNumber)
            rootdir = DATA_PATH + "games/bin/{}".format(match)
            flagOlderVersion : bool = False
            for subdir, _, files in os.walk(rootdir):
                for file in files:
                    x = re.search(r"end_state_summary_riot_" + str(seriesId) + r"_" + str(gameNumber) + ".json", file)
                    if x != None:
                        with open(os.path.join(subdir, file), "r") as json_file:
                            res : dict = json.load(json_file)
                            if "gameVersion" in list(res.keys()):
                                patch : str = res["gameVersion"]
                                flagOlderVersion = True
                        break
            
            if not(flagOlderVersion):
                patch : str = data.patch

            # print("Saving behavior analysis of match id {} {} to database".format(seriesId, matchId))

            for playerTeamOne in dataBeforeTime.gameSnapshotList[0].teams[0].players:
                summonnerName : str = playerTeamOne.playerName
                role = getRole(dataBeforeTime, summonnerName)

                gameStat : GameStat = GameStat(dataBeforeTime.getSnapShotByTime(time, gameDuration), gameDuration, begGameTime, endGameTime)

                (statDict, lanePresenceMapping) = getBehaviorData(areaMapping, gameStat, dataBeforeTime, summonnerName, time, gameDuration)

                new = False
                if not(os.path.exists(DATA_PATH + "behavior/behavior/behavior_{}.csv".format(role))):
                    new = True
                
                save_path : str = DATA_PATH + "behavior/behavior/".format(role)
                saveToDataBase(statDict, lanePresenceMapping, save_path, new, matchId, seriesId, patch, summonnerName, role, tournamentName, date, gameNumber)

            for playerTeamTwo in dataBeforeTime.gameSnapshotList[0].teams[1].players:
                summonnerName : str = playerTeamTwo.playerName
                role = getRole(dataBeforeTime, summonnerName)

                gameStat : GameStat = GameStat(dataBeforeTime.getSnapShotByTime(time, gameDuration), gameDuration, begGameTime, endGameTime)

                (statDict, lanePresenceMapping) = getBehaviorData(areaMapping, gameStat, dataBeforeTime, summonnerName, time, gameDuration)


                new = False
                if not(os.path.exists(DATA_PATH + "behavior/behavior/behavior_{}.csv".format(role))):
                    new = True
                
                save_path : str = DATA_PATH + "behavior/behavior/".format(role)
                saveToDataBase(statDict, lanePresenceMapping, save_path, new, matchId, seriesId, patch, summonnerName, role, tournamentName, date, gameNumber)

        # else:
        #     print("Behavior form game {} {} already computed".format(game.seriesId, game.gameNumber))

    # Importing data into SQLite database
    import_Behavior()

    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def getListOfDownloadableTournament(request, year):
    
    tournamentList_unicode = request.body.decode("utf-8")
    tournamentList : list = json.loads(tournamentList_unicode)
    print(tournamentList)
    
    # Check if result is already computed given the fitler list
    with open(DATA_PATH + "tournament_downloadable.json", "r") as json_file:
        temp : dict = json.load(json_file)
        filterList : list = temp["filter"]
        
        i = 0
        flag = True
        while (i < len(tournamentList) and flag):
            flag = flag and (tournamentList[i] in filterList)
            i += 1
    print(flag)
    if flag:
        # Result is already computed no need to compute it again    
        with open(DATA_PATH + "tournament_downloadable.json", "r") as json_file:
            data : dict = json.load(json_file)
            res : dict = dict()
            for tname, tid in data["data"].items():
                flag = True
                for i in range(len(tournamentList)):
                    if re.search(tournamentList[i], tname) != None:
                        res.update({tname:tid})
            return Response(res)
    
    else:
        if "League of Legends Scrims" in tournamentList:
            return Response({"League of Legends Scrims": "584178"})
        
        # We need to compute again
        regex : str = r"(?:"
        for tournament_name in tournamentList[:-1]:
            regex += str(tournament_name) + '|'
        regex += str(tournamentList[-1]) + r").*" + str(year)
        

        res : dict = dict()
        with open(DATA_PATH + "tournament_mapping.json", "r") as json_file:
            tournamentDict : dict = json.load(json_file)
            for tournamentName, tournamentId in tournamentDict.items():
                match = re.search(regex, tournamentName)
                if match:

                    _, cursorNext = get_game_seriesId_from_page_tournament("", 1, tournamentId)
                    if cursorNext != '':
                        res.update({tournamentName: tournamentId})
                    
        with open(DATA_PATH + "tournament_downloadable.json", "w") as json_file:
            res_dict : dict = {
                "data": res,
                "filter":tournamentList
            }
            json.dump(res_dict, json_file)
        
        
        return Response(res)

@api_view(['PATCH'])
def updateDatabase(request, tournamentList : str):
    # 1 Download Bins
    print(f"{' Downloading bins ' :#^50}")
    requests.patch(API_URL + "api/dataAnalysis/download/{}/".format(tournamentList))

    # 2 Save Drafts
    print(f"{' Saving Drafts ' :#^50}")
    requests.post(API_URL + "api/draft/saveDrafts/")

    # 3 Compute Behavior Stats
    print(f"{' Computing Behavior Stats ' :#^50}")
    requests.patch(API_URL + "api/dataAnalysis/computeBehaviorStats/840/")

    # 4 Update draft stats
    print(f"{' Updating draft stats ' :#^50}")
    requests.patch(API_URL + "api/draft/championStats/updateStats/{}/".format(tournamentList))

    # 5 Update champion pools
    print(f"{' Updating champion pools ' :#^50}")
    requests.patch(API_URL + "api/draft/updatePlayerStat/{}/".format(tournamentList))

    return Response(tournamentList)

@api_view(['POST'])
def getGamePositionDensity(request):
    body_unicode = request.body.decode('utf-8')
    game = json.loads(body_unicode)
    print(game)
    
    for role in ROLE_LIST:
        (data, splitList, playerNameList) = getDataPathing(game, role)
        print(splitList, playerNameList)
        makeDensityPlot(game, playerNameList, data, splitList)
    

    imgList : list = list()
    for file in os.listdir(DATA_PATH + "plots/Position/PositionDensity/{}_{}".format(game["seriesId"], game["gameNumber"])):
        path = DATA_PATH + "plots/Position/PositionDensity/{}_{}/".format(game["seriesId"], game["gameNumber"]) + file
        with open(path, "rb") as f:
            imgList.append(f.read())
            
            
    return HttpResponse(imgList, content_type="image/png")

@api_view(['GET'])
def getGameList(request, tournament):
    tournamentList : list[str] = []
    for temp in GameMetadata.objects.all():
        if not(temp.tournament in tournamentList):
            tournamentList.append(temp.tournament)
    

    if not(tournament in tournamentList):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    gameData : dict = {"data": []}
    queryGameMetadata = GameMetadata.objects.filter(tournament__exact=tournament)

    for gameMetadata in queryGameMetadata:
        temp_dict : dict = dict()
        game_str = "{} vs {} Game {} {}".format(gameMetadata.teamBlue, gameMetadata.teamRed, gameMetadata.gameNumber, gameMetadata.date)
        temp_dict["str"] = game_str
        temp_dict["seriesId"] = gameMetadata.seriesId
        temp_dict["gameNumber"] = gameMetadata.gameNumber
        gameData["data"].append(temp_dict)
    
    return Response(gameData)

@api_view(['GET'])
def getGameStatsPlayers(request, seriesId : int, gameNumber : int):
    (data, gameDuration, begGameTime, endGameTime) = getData(seriesId, gameNumber)
    
    playerIdx : dict = dict()
    resultData : dict = {
        "data" : [],
        "gameLength": gameDuration//60
    }
    i = 0
    for playerBlue in data.gameSnapshotList[0].teams[0].players:
        tempDict : dict = {
            "playerName": playerBlue.playerName,
            "DPM": [],
            "currentGold": [],
            "GPM": [],
            "XPM": [],
            "CSM": [],
        }
        resultData["data"].append(tempDict)
        playerIdx[playerBlue.playerName] = i
        i += 1

    for playerRed in data.gameSnapshotList[1].teams[1].players:
        tempDict : dict = {
            "playerName": playerRed.playerName,
            "DPM": [],
            "currentGold": [],
            "GPM": [],
            "XPM": [],
            "CSM": [],
        }
        resultData["data"].append(tempDict)
        playerIdx[playerRed.playerName] = i
        i += 1
    


    snapshotList : list[Snapshot] = [data.getSnapShotByTime(i*60, gameDuration) for i in range(gameDuration//60)]
    snapshotList.append(data.gameSnapshotList[-1])

    for gameSnapshot in snapshotList:
        for playerBlue in gameSnapshot.teams[0].players:
            if int(gameSnapshot.convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime)) == 0:
                time = 1
            else:
                time = int(gameSnapshot.convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime))
            
            DPM = 60*playerBlue.stats.totalDamageDealtChampions/time
            currentGold = playerBlue.currentGold
            if time == 1:
                GPM = 500
            else:
                GPM = 60*playerBlue.totalGold/time
            XPM = 60*playerBlue.XP/time
            CSM = 60*playerBlue.stats.minionsKilled/time
                       
            resultData["data"][playerIdx[playerBlue.playerName]]["DPM"].append(DPM)
            resultData["data"][playerIdx[playerBlue.playerName]]["currentGold"].append(currentGold)
            resultData["data"][playerIdx[playerBlue.playerName]]["GPM"].append(GPM)
            resultData["data"][playerIdx[playerBlue.playerName]]["XPM"].append(XPM)
            resultData["data"][playerIdx[playerBlue.playerName]]["CSM"].append(CSM)

        for playerRed in gameSnapshot.teams[1].players:
            if int(gameSnapshot.convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime)) == 0:
                time = 1
            else:
                time = int(gameSnapshot.convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime))

            DPM = 60*playerRed.stats.totalDamageDealtChampions/time
            currentGold = playerRed.currentGold
            if time == 1:
                GPM = 500
            else:
                GPM = 60*playerRed.totalGold/time
            XPM = 60*playerRed.XP/time
            CSM = 60*playerRed.stats.minionsKilled/time

            resultData["data"][playerIdx[playerRed.playerName]]["DPM"].append(DPM)
            resultData["data"][playerIdx[playerRed.playerName]]["currentGold"].append(currentGold)
            resultData["data"][playerIdx[playerRed.playerName]]["GPM"].append(GPM)
            resultData["data"][playerIdx[playerRed.playerName]]["XPM"].append(XPM)
            resultData["data"][playerIdx[playerRed.playerName]]["CSM"].append(CSM)

    return Response(resultData)

@api_view(['GET'])
def getGameStatsTeams(request, seriesId : int, gameNumber):
    (data, gameDuration, begGameTime, endGameTime) = getData(seriesId, gameNumber)
    resultData : dict = {
        "data" : [
            {
                "teamSide": "Blue",
                "DPM": [],
                "currentGold": [],
                "GPM": [],
                "XPM": [],
                "CSM": [],
            },
            {
                "teamSide": "Red",
                "DPM": [],
                "currentGold": [],
                "GPM": [],
                "XPM": [],
                "CSM": [],
            }
        ],
        "gameLength": gameDuration//60
    }

    snapshotList : list[Snapshot] = [data.getSnapShotByTime(i*60, gameDuration) for i in range(gameDuration//60)]
    snapshotList.append(data.gameSnapshotList[-1])

    for gameSnapshot in snapshotList:
        DPM = 0
        currentGold = 0
        GPM = 0
        XPM = 0
        CSM = 0
        for playerBlue in gameSnapshot.teams[0].players:
            if int(gameSnapshot.convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime)) == 0:
                time = 1
            else:
                time = int(gameSnapshot.convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime))
            
            DPM += 60*playerBlue.stats.totalDamageDealtChampions/time
            currentGold += playerBlue.currentGold

            if time == 1:
                GPM += 500
            else:
                GPM += 60*playerBlue.totalGold/time
            
            XPM += 60*playerBlue.XP/time
            CSM += 60*playerBlue.stats.minionsKilled/time

        resultData["data"][0]["DPM"].append(DPM/5)
        resultData["data"][0]["currentGold"].append(currentGold/5)
        resultData["data"][0]["GPM"].append(GPM/5)
        resultData["data"][0]["XPM"].append(XPM/5)
        resultData["data"][0]["CSM"].append(CSM/5)

        DPM = 0
        currentGold = 0
        GPM = 0
        XPM = 0
        CSM = 0
        for playerRed in gameSnapshot.teams[1].players:
            if int(gameSnapshot.convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime)) == 0:
                time = 1
            else:
                time = int(gameSnapshot.convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime))
            
            DPM += 60*playerRed.stats.totalDamageDealtChampions/time
            currentGold += playerRed.currentGold

            if time == 1:
                GPM += 500
            else:
                GPM += 60*playerRed.totalGold/time
            
            XPM += 60*playerRed.XP/time
            CSM += 60*playerRed.stats.minionsKilled/time

        resultData["data"][1]["DPM"].append(DPM/5)
        resultData["data"][1]["currentGold"].append(currentGold/5)
        resultData["data"][1]["GPM"].append(GPM/5)
        resultData["data"][1]["XPM"].append(XPM/5)
        resultData["data"][1]["CSM"].append(CSM/5)
    
    return Response(resultData)
            
@api_view(['DELETE'])
def delete_all_behavior(request):
    queryTop = BehaviorTop.objects.all()
    for res in tqdm(queryTop):
        res.delete()

    queryJungle = BehaviorJungle.objects.all()
    for res in tqdm(queryJungle):
        res.delete()

    queryMid = BehaviorMid.objects.all()
    for res in tqdm(queryMid):
        res.delete()

    queryADC = BehaviorADC.objects.all()
    for res in tqdm(queryADC):
        res.delete()

    querySupport = BehaviorSupport.objects.all()
    for res in tqdm(querySupport):
        res.delete()

    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def getProximityMatrix(request, seriesId : int, gameNumber : int, time : int):
    (data, gameDuration, _, _) = getData(seriesId, gameNumber)

    # usually time = 840s i.e 14min
    # Splitting our data so we get the interval between [840s; gameDuration]
    splitList : list[int] = [120, time, gameDuration]
    splittedDataset : list[SeparatedData] = data.splitData(gameDuration, splitList)

    dataBeforeTime : SeparatedData = splittedDataset[1] # Getting the wanted interval
    proximityMatrixBlue : list[list] = getProxomityMatrix(dataBeforeTime, 0)
    proximityMatrixRed : list[list] = getProxomityMatrix(dataBeforeTime, 1)

    teamBlue : Team = dataBeforeTime.gameSnapshotList[0].teams[0]
    teamRed : Team = dataBeforeTime.gameSnapshotList[0].teams[1]

    fig, axes = plt.subplots(ncols=1, figsize=(8,6))

    im = axes.imshow(proximityMatrixBlue, cmap="RdBu_r", vmax=1, vmin=0, aspect='auto')
    for (i, j), z in np.ndenumerate(proximityMatrixBlue):
        axes.text(j, i, str(round(z, 2)), ha="center", va="center")
    
    axes.set_title("Proximity Matrix {}".format(teamBlue.getTeamName(seriesId)))
    axes.set_xticks(np.arange(5))
    axes.set_yticks(np.arange(5))
    axes.set_xticklabels(teamBlue.getPlayerList())
    axes.set_yticklabels(teamBlue.getPlayerList())

    plt.tight_layout()
    cb = fig.colorbar(im, ax=axes, location='right', label="proximity")
    plt.savefig(DATA_PATH)
    

    return Response(status=status.HTTP_200_OK)