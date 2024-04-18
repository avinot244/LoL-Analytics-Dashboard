from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from behaviorADC.models import BehaviorTop, BehaviorJungle, BehaviorMid, BehaviorADC, BehaviorSupport

from .globals import DATA_PATH, BLACKLIST
from .packages.api_calls.GRID.api_calls import *
from .utils import isGameDownloaded
from .packages.utils_stuff.utils_func import getData, getSummaryData, getRole
from .packages.Parsers.EMH.Summary.SummaryData import SummaryData
from .packages.Parsers.Separated.Game.SeparatedData import SeparatedData
from .packages.AreaMapping.AreaMapping import AreaMapping
from .packages.GameStat import GameStat
from .packages.BehaviorAnalysisRunner.behaviorAnalysis import getBehaviorData, saveToDataBase

from Draft.models import DraftPlayerPick


from .models import GameMetadata

import json
import pandas as pd

@api_view(['PATCH'])
def download_latest(request, rawTournamentList : str):
    print("yo")
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
        seriesIdList = get_all_game_seriesId_tournament(tournament_id, 200)
        
        
        for seriesId in seriesIdList:
            if not(seriesId in BLACKLIST):
                dlDict : dict = get_all_download_links(seriesId)
                i = 0
                print("\tChecking game of seriesId :", seriesId)
                for downloadDict in dlDict['files']:
                    fileType = downloadDict["fileName"].split(".")[-1]
                    fileName = downloadDict["fileName"].split(".")[0]

                    if fileType != "rofl" and downloadDict["status"] == "ready":
                        if i > 1:
                            # The first 2 files are global info about the Best-of
                            # We have 4 files per games
                            # We add 1 to start the gameNumber list at 1
                            
                            gameNumber = (i-2)//4 + 1
                            if not(isGameDownloaded(int(seriesId), gameNumber)) and gameNumber < get_nb_games_seriesId(seriesId) + 1:

                                path : str = DATA_PATH + "games/bin/" + "{}_{}_{}/".format(seriesId, "ESPORTS", gameNumber)
                                print("\t\tDownloading {} files".format(fileName))
                                download_from_link(downloadDict['fullURL'], fileName, path, fileType)

                        else:
                            for gameNumber in range(1, get_nb_games_seriesId(seriesId) + 1):
                                if not(isGameDownloaded(int(seriesId), gameNumber)):
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
                    summaryData : SummaryData = getSummaryData(DATA_PATH + "games/bin/{}_ESPORTS_{}".format(seriesId, gameNumberIt))

                    (data, _, _, _) = getData(int(seriesId), gameNumberIt)
                    patch : str = summaryData.patch
                    teamBlue : str = data.gameSnapshotList[0].teams[0].getTeamName()
                    teamRed : str = data.gameSnapshotList[1].teams[0].getTeamName()
                    winningTeam : int = data.winningTeam

                    
                    # Saving game metadata to SQLite datbase
                    gameMetadata : GameMetadata = GameMetadata(date=date, name=name, patch=patch, seriesId=seriesId, teamBlue=teamBlue, teamRed=teamRed, winningTeam=winningTeam, gameNumber=gameNumberIt)
                    gameMetadata.save()
    
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
                summaryData : SummaryData = getSummaryData(DATA_PATH + "games/bin/{}_ESPORTS_{}".format(seriesId, gameNumberIt))

                (data, _, _, _) = getData(int(seriesId), gameNumberIt)
                patch : str = summaryData.patch
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

    for game in queryAllGames:
        if not(BehaviorADC.objects.filter(
            date=game.date,
            seriesId=game.seriesId,
            gameNumber=game.gameNumber
        ).count() > 0):
            seriesId : int = game.seriesId
            gameNumber : int = game.gameNumber
            (data, gameDuration, begGameTime, endGameTime) = getData(seriesId, gameNumber)

            match : str = "{}_ESPORTS_{}".format(seriesId, gameNumber)
            rootdir : str = DATA_PATH + "games/bin/{}".format(match)
            summaryData : SummaryData = getSummaryData(rootdir)

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
            patch : str = summaryData.gameVersion
            print("Saving behavior analysis of match id {} {} to database".format(seriesId, matchId))

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

        else:
            print("Behavior form game {} {} already computed".format(game.seriesId, game.gameNumber))

    return Response(status=status.HTTP_200_OK)