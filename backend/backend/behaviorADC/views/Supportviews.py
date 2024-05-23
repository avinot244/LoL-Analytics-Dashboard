from django.shortcuts import render
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from behaviorADC.models import BehaviorSupport
from behaviorADC.serializers import *
from behaviorADC.globals import API_URL
from behaviorADC.utils import getDataBase, compute

from dataAnalysis.globals import DATE_LIMIT

import pandas as pd
import requests
from datetime import datetime


@api_view(['GET'])
def behaviorSupport_get_player_list(request, patch, scrim):
    if scrim == 0:
        allObjects = BehaviorSupport.objects.filter(patch__contains=patch).filter(~Q(tournament="League of Legends Scrims"))
    else:
        allObjects = BehaviorSupport.objects.filter(patch__contains=patch, tournament__exact="League of Legends Scrims")
    summonnerNameList : list = list()

    for SupportObject in allObjects:
        summonnerNameList.append(SupportObject.summonnerName)
    
    df = pd.DataFrame({"summonnerName": summonnerNameList})
    return Response(df["summonnerName"].unique())

@api_view(['GET'])
def behaviorSupport_get_player_list_tournament(request, patch, tournament):
    if tournament == "League of Legends Scrims":
        allObjects = BehaviorSupport.objects.filter(patch__contains=patch, tournament__exact=tournament, date__gte=DATE_LIMIT)
    else:
        allObjects = BehaviorSupport.objects.filter(patch__contains=patch, tournament__exact=tournament)
    summonnerNameList : list = list()

    for SupportObject in allObjects:
        if not(SupportObject.summonnerName in summonnerNameList):
            summonnerNameList.append(SupportObject.summonnerName)
        
    return Response(summonnerNameList)

@api_view(['PATCH'])
def behaviorSupport_updatePatch(request):
    csv_file_path = "./databases/behavior/behavior/behavior_Support.csv"
    df = pd.read_csv(csv_file_path, sep=";")

    for _, row in df.iterrows():
        queryResult = BehaviorSupport.objects.filter(seriesId__exact=row["SeriesId"], summonnerName__exact=row["SummonnerName"], matchId__exact=row["MatchId"])
        print(queryResult)

        data = BehaviorSupport.objects.get(seriesId=row["SeriesId"], summonnerName=row["SummonnerName"], matchId=row["MatchId"])
        data.delete()
        data.patch = row["Patch"]
        data.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def behaviorSupport_stats(request, summonnerName):

    summonnerNameList : list = list()
    allObjects = BehaviorSupport.objects.all()
    for res in allObjects:
        summonnerNameList.append(res.summonnerName)

    df = pd.DataFrame({"summonnerName": summonnerNameList})


    if not(summonnerName in df["summonnerName"].unique().tolist()) :
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    queryResult = BehaviorSupport.objects.filter(summonnerName__exact=summonnerName)
    serializer = BehaviorSupportSerializer(queryResult,  context={"request": request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def behaviorSupport_stats_tournament(request, summonnerName, tournament):
    summonnerNameList : list = list()
    if tournament == "League of Legends Scrims":
        allObjects = BehaviorSupport.objects.filter(tournament__exact=tournament, date__gte=DATE_LIMIT)
    else:
        allObjects = BehaviorSupport.objects.filter(tournament__exact=tournament)
    for res in allObjects:
        if not(res.summonnerName in summonnerNameList):
            summonnerNameList.append(res.summonnerName)
    if not(summonnerName in summonnerNameList):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    queryResult = BehaviorSupport.objects.filter(summonnerName__exact=summonnerName, tournament__exact=tournament)
    serializer = BehaviorSupportSerializer(queryResult, context={"request": request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def behaviorSupport_stats_latest(request, summonnerName, limit, tournament):
    summonnerNameList : list = list()
    allObjects = BehaviorSupport.objects.all()
    for res in allObjects:
        summonnerNameList.append(res.summonnerName)

    df = pd.DataFrame({"summonnerName": summonnerNameList})

    if not(summonnerName in df["summonnerName"].unique().tolist()) :
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    queryResult = BehaviorSupport.objects.filter(summonnerName__exact=summonnerName, tournament__exact=tournament).order_by("-seriesId")[:int(limit)]
    serializer = BehaviorSupportSerializer(queryResult,  context={"request": request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def behaviorSupport_stats_patch(request, summonnerName, patch, tournament):
    #Getting all of the unique patches
    queryListPatch = BehaviorSupport.objects.all()
    patchList : list = list()

    for res in queryListPatch:
        tempPatch = res.patch.split(".")[0] + "." + res.patch.split(".")[1]
        patchList.append(tempPatch)
    dfPatch = pd.DataFrame({"patch": patchList})
    dfPatchUnique = dfPatch["patch"].unique()

    if not(patch in dfPatchUnique.tolist()):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    queryResult = BehaviorSupport.objects.filter(summonnerName__exact=summonnerName, patch__contains=patch, tournament__exact=tournament)
    serializer = BehaviorSupportSerializer(queryResult, context={"request": request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def behaviorSupport_stats_game(request, summonnerName, seriesId, gameNumber):
    summonnerNameList : list = list()
    allObjects = BehaviorSupport.objects.filter(seriesId__exact=seriesId, gameNumber__exact=gameNumber)
    for res in allObjects:
        print(res)
        if not(res.summonnerName in summonnerNameList):
            summonnerNameList.append(res.summonnerName)
    if not(summonnerName in summonnerNameList):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    queryResult = BehaviorSupport.objects.filter(summonnerName__exact=summonnerName, seriesId__exact=seriesId, gameNumber__exact=gameNumber)
    serializer = BehaviorSupportSerializer(queryResult, context={"request": request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def behaviorSupport_behavior_latest(request, summonnerName, limit, uuid, wantedTournament, comparisonTournament):
    tournamentDict = {
        "wanted" : wantedTournament,
        "comparison" : comparisonTournament,
    }

    # Checking if the tournament in tournamentDict are in our database
    response = requests.get(
        API_URL + 'api/dataAnalysis/tournament/getList'
    )
    tournamentListDB : list = list()
    for tournament in response.json():
        tournamentListDB.append(tournament)
    
    for key in tournamentDict.keys():
        flag : bool = tournamentDict[key] in tournamentListDB
    
        if not(flag):
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # Getting the db we want given a player 
    response = requests.get(
        API_URL + "api/behavior/Support/stats/latest/{}/{}/{}/".format(summonnerName, limit, tournamentDict["wanted"])
    )
    wantedDB = pd.DataFrame(response.json())
    transformed_wantedDB_scaled = compute(wantedDB, uuid, tournamentDict, header_offset=8, role="Support")
    return Response(transformed_wantedDB_scaled)

@api_view(['GET'])
def behaviorSupport_behavior_patch(request, summonnerName, patch, uuid, wantedTournament, comparisonTournament):
    tournamentDict = {
        "wanted" : wantedTournament,
        "comparison" : comparisonTournament,
    }

    # Checking if the tournament in tournamentDict are in our database
    response = requests.get(
        API_URL + 'api/dataAnalysis/tournament/getList'
    )
    tournamentListDB : list = list()
    for tournament in response.json():
        tournamentListDB.append(tournament)
    
    for key in tournamentDict.keys():
        flag : bool = tournamentDict[key] in tournamentListDB
    
        if not(flag):
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # Getting the db we want given a player and the patch
    response = requests.get(
        API_URL + "api/behavior/Support/stats/patch/{}/{}/{}/".format(summonnerName, patch, tournamentDict["wanted"])
    )
    wantedDB = pd.DataFrame(response.json())
    transformed_wantedDB_scaled = compute(wantedDB, uuid, tournamentDict, header_offset=8, role="Support")
    return Response(transformed_wantedDB_scaled)

@api_view(['GET'])
def behaviorSupport_behavior_tournament(request, summonnerName, uuid, wantedTournament, comparisonTournament):
    tournamentDict = {
        "wanted": wantedTournament,
        "comparison": comparisonTournament,
    }

    # Checking if the tournament in tournamentDict are in our database
    response = requests.get(
        API_URL + 'api/dataAnalysis/tournament/getList'
    )
    tournamentListDB : list = list()
    for tournament in response.json():
        tournamentListDB.append(tournament)
    
    for key in tournamentDict.keys():
        flag : bool = tournamentDict[key] in tournamentListDB
    
        if not(flag):
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # Getting the db we want given a player and a tournament
    response = requests.get(
        API_URL + "api/behavior/Support/stats/{}/{}/".format(summonnerName, tournamentDict["wanted"])
    )
    wantedDB = pd.DataFrame(response.json())
    transformed_wantedDB_scaled = compute(wantedDB, uuid, tournamentDict, header_offset=8, role="Support")
    return Response(transformed_wantedDB_scaled)

@api_view(['GET'])
def behaviorSupport_behavior_game(request, summonnerName, uuid, seriesId, gameNumber, wantedTournament, comparisonTournament):
    tournamentDict = {
        "wanted": wantedTournament,
        "comparison": comparisonTournament,
    }

    # Getting the db we want given a player and a tournament
    response = requests.get(
        API_URL + "api/behavior/Support/stats/game/{}/{}/{}/".format(summonnerName, seriesId, gameNumber)
    )
    wantedDB = pd.DataFrame(response.json())
    transformed_wantedDB_scaled = compute(wantedDB, uuid, tournamentDict, header_offset=8, role="Support")
    return Response(transformed_wantedDB_scaled)

@api_view(['GET'])
def behaviorSupport_behavior_singleGamesLatest(request, summonnerName, uuid, limit, wantedTournament, comparisonTournament):
    gameResponse = requests.get(
        API_URL + "api/behavior/Support/stats/latest/{}/{}/{}/".format(summonnerName, limit, wantedTournament)
    )

    gameList : list = list(gameResponse.json())

    resultList : list = list()

    for gameObject in gameList:
        behaviorGame = requests.get(
            API_URL + "api/behavior/Support/compute/{}/{}/{}/{}/{}/{}/".format(summonnerName, uuid, gameObject["seriesId"], gameObject["gameNumber"], wantedTournament, comparisonTournament)
        )
        resultList.append(behaviorGame.json())

    return Response(resultList)
    
@api_view(['DELETE'])
def behaviorSupport_deleteDuplicates(request):
    csv_file_path = "./databases/behavior/behavior/behavior_Support.csv"
    df = pd.read_csv(csv_file_path, sep=";")

    for _, row in df.iterrows():
        queryResult = BehaviorSupport.objects.filter(seriesId__exact=row["SeriesId"], summonnerName__exact=row["SummonnerName"], matchId__exact=row["MatchId"])
        if len(queryResult) > 1:
            queryResult[0].delete()
    
    return Response(status=status.HTTP_200_OK)