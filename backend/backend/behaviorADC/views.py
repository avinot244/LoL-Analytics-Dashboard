from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import BehaviorADC
from .serializers import *
from .globals import BEHAVIOR_ADC_HEADER, DATA_PATH
from .api_calls.GRID.api_calls import get_all_game_seriesId_tournament

import os
import pandas as pd
import json
import re

@api_view(['GET'])
def behaviorADC_get_player_list(request):
    allObjects = BehaviorADC.objects.all()
    summonnerNameList : list = list()

    for ADCObject in allObjects:
        summonnerNameList.append(ADCObject.summonnerName)
    
    df = pd.DataFrame({"summonnerName": summonnerNameList})
    return Response(df["summonnerName"].unique())

@api_view(['PATCH'])
def behaviorADC_updatePatch(request):
    csv_file_path = "./databases/behavior/behavior/behavior_ADC.csv"
    df = pd.read_csv(csv_file_path, sep=";")

    for _, row in df.iterrows():
        queryResult = BehaviorADC.objects.filter(seriesId__exact=row["SeriesId"], summonnerName__exact=row["SummonnerName"], matchId__exact=row["MatchId"])
        print(queryResult)

        data = BehaviorADC.objects.get(seriesId=row["SeriesId"], summonnerName=row["SummonnerName"], matchId=row["MatchId"])
        data.delete()
        data.patch = row["Patch"]
        data.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


#TODO: behaviorADC_download view
@api_view(['PATCH'])
def behaviorADC_download(request, rawTournamentList : str):
    if rawTournamentList.__contains__(','):
        wantedTournamentList : list = rawTournamentList.split(",")
        
        # Getting the list of tournament in our database
        tournamentList : list = list()
        queryTournamentList = BehaviorADC.objects.all()
        for res in queryTournamentList:
            tournamentList.append(res.tournament)
        df = pd.DataFrame({'tournaments': tournamentList})
        tournamentList = df['tournaments'].unique().tolist()

        # Testing if the tournament list are in our database
        for res in wantedTournamentList:
            if not(res in tournamentList):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        
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
        
        
        print(wantedTournamentMapping)
        for tournament_name, tournament_id in wantedTournamentMapping.items():
            print(tournament_id, tournament_name)
            seriesIdList = get_all_game_seriesId_tournament(tournament_id, 200)
            print(seriesIdList)

        return Response(wantedTournamentMapping)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def behaviorADC_stats(request, summonnerName):

    summonnerNameList : list = list()
    allObjects = BehaviorADC.objects.all()
    for res in allObjects:
        summonnerNameList.append(res.summonnerName)

    df = pd.DataFrame({"summonnerName": summonnerNameList})


    if not(summonnerName in df["summonnerName"].unique().tolist()) :
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    queryResult = BehaviorADC.objects.filter(summonnerName__exact=summonnerName)
    serializer = BehaviorADCSerializer(queryResult,  context={"request": request}, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def behaviorADC_stats_latest(request, summonnerName, limit, tournament):
    summonnerNameList : list = list()
    allObjects = BehaviorADC.objects.all()
    for res in allObjects:
        summonnerNameList.append(res.summonnerName)

    df = pd.DataFrame({"summonnerName": summonnerNameList})


    if not(summonnerName in df["summonnerName"].unique().tolist()) :
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    queryResult = BehaviorADC.objects.filter(summonnerName__exact=summonnerName, tournament__exact=tournament).all()[:int(limit)]
    serializer = BehaviorADCSerializer(queryResult,  context={"request": request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def behaviorADC_stats_patch(request, summonnerName, patch, tournament):
    #Getting all of the unique patches
    queryListPatch = BehaviorADC.objects.all()
    patchList : list = list()

    for res in queryListPatch:
        tempPatch = res.patch.split(".")[0] + "." + res.patch.split(".")[1]
        patchList.append(tempPatch)
    dfPatch = pd.DataFrame({"patch": patchList})
    dfPatchUnique = dfPatch["patch"].unique()

    if not(patch in dfPatchUnique.tolist()):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    queryResult = BehaviorADC.objects.filter(summonnerName__exact=summonnerName, patch__contains=patch, tournament__exact=tournament)
    serializer = BehaviorADCSerializer(queryResult, context={"request": request}, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def get_listPatch(request):
    queryResult = BehaviorADC.objects.all()
    patchList : list = list()

    for res in queryResult:
        patch = res.patch.split(".")[0] + "." + res.patch.split(".")[1]
        patchList.append(patch)
    df = pd.DataFrame({"patch": patchList})

    return Response(df["patch"].unique())

@api_view(['GET'])
def get_listTournaments(request):
    queryResult = BehaviorADC.objects.all()
    tournamentList : list = list()

    for res in queryResult:
        tournamentList.append(res.tournament)
    df = pd.DataFrame({'tournaments': tournamentList})
    return Response(df['tournaments'].unique())






