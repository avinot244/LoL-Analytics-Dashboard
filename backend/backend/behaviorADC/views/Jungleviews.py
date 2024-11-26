from django.shortcuts import render
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from behaviorADC.models import BehaviorJungle
from behaviorADC.serializers import *
from behaviorADC.globals import API_URL
from behaviorADC.utils import getDataBase, compute

from dataAnalysis.globals import DATE_LIMIT

import pandas as pd
import json
import requests

@api_view(['GET'])
def behaviorJungle_get_player_list(request, patch, scrim):
    if scrim == 0:
        allObjects = BehaviorJungle.objects.filter(patch__contains=patch).filter(~Q(tournament="League of Legends Scrims"))
    else:
        allObjects = BehaviorJungle.objects.filter(patch__contains=patch, tournament__exact="League of Legends Scrims")
    summonnerNameList : list = list()

    for JungleObject in allObjects:
        summonnerNameList.append(JungleObject.summonnerName)
    
    df = pd.DataFrame({"summonnerName": summonnerNameList})
    return Response(df["summonnerName"].unique())

@api_view(['GET'])
def behaviorJungle_get_player_list_tournament(request, patch, tournament):
    if tournament == "League of Legends Scrims":
        allObjects = BehaviorJungle.objects.filter(patch__contains=patch, tournament__exact=tournament, date__gte=DATE_LIMIT)
    else:
        allObjects = BehaviorJungle.objects.filter(patch__contains=patch, tournament__exact=tournament)
    summonnerNameList : list = list()

    for JungleObject in allObjects:
        if not(JungleObject.summonnerName in summonnerNameList):
            summonnerNameList.append(JungleObject.summonnerName)
        
    return Response(summonnerNameList)

@api_view(['PATCH'])
def behaviorJungle_updatePatch(request):
    csv_file_path = "./databases/behavior/behavior/behavior_Jungle.csv"
    df = pd.read_csv(csv_file_path, sep=";")

    for _, row in df.iterrows():
        queryResult = BehaviorJungle.objects.filter(seriesId__exact=row["SeriesId"], summonnerName__exact=row["SummonnerName"], matchId__exact=row["MatchId"])
        print(queryResult)

        data = BehaviorJungle.objects.get(seriesId=row["SeriesId"], summonnerName=row["SummonnerName"], matchId=row["MatchId"])
        data.delete()
        data.patch = row["Patch"]
        data.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def behaviorJungle_stats(request, summonnerName):

    summonnerNameList : list = list()
    allObjects = BehaviorJungle.objects.all()
    for res in allObjects:
        summonnerNameList.append(res.summonnerName)

    df = pd.DataFrame({"summonnerName": summonnerNameList})


    if not(summonnerName in df["summonnerName"].unique().tolist()) :
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    queryResult = BehaviorJungle.objects.filter(summonnerName__exact=summonnerName)
    serializer = BehaviorJungleSerializer(queryResult,  context={"request": request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def behaviorJungle_stats_tournament(request, summonnerName, tournament):
    summonnerNameList : list = list()
    if tournament == "League of Legends Scrims":
        allObjects = BehaviorJungle.objects.filter(tournament__exact=tournament, date__gte=DATE_LIMIT)
    else:
        allObjects = BehaviorJungle.objects.filter(tournament__exact=tournament)
    
    for res in allObjects:
        if not(res.summonnerName in summonnerNameList):
            summonnerNameList.append(res.summonnerName)
    if not(summonnerName in summonnerNameList):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    queryResult = BehaviorJungle.objects.filter(summonnerName__exact=summonnerName, tournament__exact=tournament)
    serializer = BehaviorJungleSerializer(queryResult, context={"request": request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def behaviorJungle_stats_latest(request, summonnerName, limit, tournament):
    summonnerNameList : list = list()
    allObjects = BehaviorJungle.objects.all()
    for res in allObjects:
        summonnerNameList.append(res.summonnerName)

    df = pd.DataFrame({"summonnerName": summonnerNameList})

    print(df["summonnerName"].unique().tolist())

    if not(summonnerName in df["summonnerName"].unique().tolist()) :
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    queryResult = BehaviorJungle.objects.filter(summonnerName__exact=summonnerName, tournament__exact=tournament).order_by("-seriesId")[:int(limit)]
    serializer = BehaviorJungleSerializer(queryResult,  context={"request": request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def behaviorJungle_stats_patch(request, summonnerName, patch, tournament):
    #Getting all of the unique patches
    queryListPatch = BehaviorJungle.objects.all()
    patchList : list = list()

    for res in queryListPatch:
        tempPatch = res.patch.split(".")[0] + "." + res.patch.split(".")[1]
        patchList.append(tempPatch)
    dfPatch = pd.DataFrame({"patch": patchList})
    dfPatchUnique = dfPatch["patch"].unique()

    if not(patch in dfPatchUnique.tolist()):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    queryResult = BehaviorJungle.objects.filter(summonnerName__exact=summonnerName, patch__contains=patch, tournament__exact=tournament)
    serializer = BehaviorJungleSerializer(queryResult, context={"request": request}, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def behaviorJungle_stats_game(request, summonnerName, seriesId, gameNumber):
    summonnerNameList : list = list()
    allObjects = BehaviorJungle.objects.filter(seriesId__exact=seriesId, gameNumber__exact=gameNumber)
    for res in allObjects:
        print(res)
        if not(res.summonnerName in summonnerNameList):
            summonnerNameList.append(res.summonnerName)
    if not(summonnerName in summonnerNameList):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    queryResult = BehaviorJungle.objects.filter(summonnerName__exact=summonnerName, seriesId__exact=seriesId, gameNumber__exact=gameNumber)
    serializer = BehaviorJungleSerializer(queryResult, context={"request": request}, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def behaviorJungle_behavior_latest(request, summonnerName, limit, uuid, wantedTournament, comparisonTournament):
    tournamentDict = {
        "wanted" : wantedTournament,
        "comparison" : [comparisonTournament],
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
        API_URL + "api/behavior/Jungle/stats/latest/{}/{}/{}/".format(summonnerName, limit, tournamentDict["wanted"])
    )
    wantedDB = pd.DataFrame(response.json())
    transformed_wantedDB_scaled = compute(wantedDB, uuid, tournamentDict, header_offset=8, role="Jungle")
    return Response(transformed_wantedDB_scaled)

@api_view(['GET'])
def behaviorJungle_behavior_patch(request, summonnerName, patch, uuid, wantedTournament, comparisonTournament):
    tournamentDict = {
        "wanted" : wantedTournament,
        "comparison" : [comparisonTournament],
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
        API_URL + "api/behavior/Jungle/stats/patch/{}/{}/{}/".format(summonnerName, patch, tournamentDict["wanted"])
    )
    wantedDB = pd.DataFrame(response.json())
    transformed_wantedDB_scaled = compute(wantedDB, uuid, tournamentDict, header_offset=8, role="Jungle")
    return Response(transformed_wantedDB_scaled)

@api_view(['GET'])
def behaviorJungle_behavior_tournament(request, summonnerName, uuid, wantedTournament, comparisonTournament):
    tournamentDict = {
        "wanted": wantedTournament,
        "comparison": [comparisonTournament],
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
        API_URL + "api/behavior/Jungle/stats/{}/{}/".format(summonnerName, tournamentDict["wanted"])
    )
    wantedDB = pd.DataFrame(response.json())
    transformed_wantedDB_scaled = compute(wantedDB, uuid, tournamentDict, header_offset=8, role="Jungle")
    return Response(transformed_wantedDB_scaled)

@api_view(['GET'])
def behaviorJungle_behavior_game(request, summonnerName, uuid, seriesId, gameNumber, wantedTournament, comparisonTournament):
    print("Behavior Game")
    tournamentDict = {
        "wanted": wantedTournament,
        "comparison": [comparisonTournament],
    }

    # Getting the db we want given a player and a tournament
    response = requests.get(
        API_URL + "api/behavior/Jungle/stats/game/{}/{}/{}/".format(summonnerName, seriesId, gameNumber)
    )
    wantedDB = pd.DataFrame(response.json())
    print(wantedDB)
    transformed_wantedDB_scaled = compute(wantedDB, uuid, tournamentDict, header_offset=8, role="Jungle")
    return Response(transformed_wantedDB_scaled)

@api_view(['GET'])
def behaviorJungle_behavior_singleGamesLatest(request, summonnerName, uuid, limit, wantedTournament, comparisonTournament):
    gameResponse = requests.get(
        API_URL + "api/behavior/Jungle/stats/latest/{}/{}/{}/".format(summonnerName, limit, wantedTournament)
    )

    gameList : list = list(gameResponse.json())

    resultList : list = list()

    for gameObject in gameList:
        behaviorGame = requests.get(
            API_URL + "api/behavior/Jungle/compute/{}/{}/{}/{}/{}/{}/".format(summonnerName, uuid, gameObject["seriesId"], gameObject["gameNumber"], wantedTournament, comparisonTournament)
        )
        resultList.append(behaviorGame.json())

    return Response(resultList)

@api_view(['PATCH'])
def behaviorJungle_behavior_multiple_tournaments(request):
    print(request.body)
    data = json.loads(request.body)
    wantedTournaments : list[str] = list()
    model_uuid : str = ""
    try:
        wantedTournaments = data["wantedTournaments"]
        model_uuid = data["model_uuid"]
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # Get the list of all players in the list of wanted tournaments
    df_list : list[pd.DataFrame] = list()
    for tournament in wantedTournaments:
        queryResult = BehaviorJungle.objects.filter(tournament__exact=tournament)
        serializer = BehaviorJungleSerializer(queryResult, context={"request": request}, many=True)
        df : pd.DataFrame = pd.DataFrame(serializer.data)
        df_list.append(df)
    
    df_all_player : pd.DataFrame = pd.concat(df_list)

    # Transform and scale the database
    tournamentDict = {
        "wanted": wantedTournaments,
        "comparison": wantedTournaments,
    }
    transformed_result_scaled : pd.DataFrame = compute(df_all_player, model_uuid, tournamentDict, header_offset=8, role="Jungle")
    
    # Make the average for each player
    # Get the list of players
    summonnerNameList : list = list()
    for tournament in wantedTournaments:
        allObjects = BehaviorJungle.objects.filter(tournament__exact=tournament)
        for res in allObjects:
            if not(res.summonnerName in summonnerNameList):
                summonnerNameList.append(res.summonnerName)

    # make the average by summonnerName
    df_list_avg : list[pd.DataFrame] = list()
    columns_to_scale_on : list[str] = transformed_result_scaled.columns[8:].to_list()
    for summonnerName in summonnerNameList:
        df_player : pd.DataFrame = transformed_result_scaled[transformed_result_scaled["summonnerName"] == summonnerName]
        df_player = df_player[columns_to_scale_on].mean()
        
        data : dict = {
            "summonnerName": summonnerName
        }
        for col in columns_to_scale_on:
            data[col] = [df_player[col]]
        
        temp = pd.DataFrame(data)
        df_list_avg.append(temp)
    
    result : pd.DataFrame = pd.concat(df_list_avg)
    
    return Response(result)