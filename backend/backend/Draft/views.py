from django.shortcuts import render
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import DraftPickOrder, DraftPlayerPick, ChampionDraftStats
from .serializer import DraftPickOrderSerializer, ChampionDraftStatsSerializer

from dataAnalysis.packages.api_calls.GRID.api_calls import get_tournament_from_seriesId
from dataAnalysis.packages.api_calls.DDragon.api_calls import get_champion_mapping_key_reversed
from dataAnalysis.packages.utils_stuff.utils_func import getData
from dataAnalysis.globals import DATA_PATH, API_URL
from dataAnalysis.models import GameMetadata
from dataAnalysis.serializer import GameMetadataSerialize

from .packages.utils import isDraftDownloaded
from .packages.championStats_utils import *

import pandas as pd
import requests
import os

@api_view(['POST'])
def saveDrafts(request):
    data_metadata : pd.DataFrame = pd.read_csv(DATA_PATH + "games/data_metadata.csv", sep=";")

    for idx, row in data_metadata.iterrows():
        file_name : str = row["Name"]
        gameNumber : int = int(file_name.split("_")[2][0])
        seriesId : int = row["SeriesId"]
        patch : str = row["Patch"]
        tournament : str = get_tournament_from_seriesId(seriesId)
        teamBlue = row["teamBlue"]
        teamRed = row["teamRed"]
        

        (data, _, _, _) = getData(seriesId, gameNumber)
        date = row["Date"]

        # Saving the draft into our CSV database

        # Checking if the database exists
        if os.path.exists(DATA_PATH + "drafts/draft_pick_order.csv") and os.path.exists(DATA_PATH + "drafts/draft_player_picks.csv"):
            # Checking if the draft we want to save is already in our database
            if not(isDraftDownloaded(seriesId, gameNumber, DATA_PATH + "drafts/draft_pick_order.csv")):
                if not(isDraftDownloaded(seriesId, gameNumber, DATA_PATH + "drafts/draft_player_picks.csv")):
                    # Saving the draft into our csv database
                    print(seriesId)
                    data.draftToCSV(DATA_PATH + "drafts/", new=False, patch=patch, seriesId=seriesId, tournament=tournament, gameNumber=gameNumber, date=date, teamBlue=teamBlue, teamRed=teamRed)
        else:
            print(seriesId)
            data.draftToCSV(DATA_PATH + "drafts/", new=True, patch=patch, seriesId=seriesId, tournament=tournament, gameNumber=gameNumber, date=date, teamBlue=teamBlue, teamRed=teamRed)

    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def getLatestDraft(request, limit, scrimStr):
    scrim : int = int(scrimStr)
    if not(scrim == 0 or scrim == 1):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if scrim == 0:
        draftQuery = DraftPickOrder.objects.filter(tournament__exact="League of Legends Scrims").order_by("-seriesId")[:limit]
        serializer = DraftPickOrderSerializer(draftQuery, context={"request": request}, many=True)
    else:
        draftQuery = DraftPickOrder.objects.filter(~Q(tournament="League of Legends Scrims")).order_by("-seriesId")[:limit]
        serializer = DraftPickOrderSerializer(draftQuery, context={"request": request}, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def getDraftPatch(request, patch, scrimStr):
    scrim : int = int(scrimStr)
    
    #Getting all of the unique patches
    queryListPatch = GameMetadata.objects.all()
    patchList : list = list()

    for res in queryListPatch:
        tempPatch = res.patch.split(".")[0] + "." + res.patch.split(".")[1]
        patchList.append(tempPatch)
    
    dfPatch = pd.DataFrame({"patch": patchList})
    dfPatchUnique = dfPatch["patch"].unique()

    if not(patch in dfPatchUnique.tolist()):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if not(scrim == 0 or scrim == 1):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if scrim == 0:
        draftQuery = DraftPickOrder.objects.filter(tournament__exact="League of Legends Scrims", patch__contains=patch)
        serializer = DraftPickOrderSerializer(draftQuery, context={"request": request}, many=True)
    else:
        draftQuery = DraftPickOrder.objects.filter(~Q(tournament="League of Legends Scrims"), patch__contains=patch)
        serializer = DraftPickOrderSerializer(draftQuery, context={"request": request}, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def getDraftTournament(request, tournament):
    queryListTournament = DraftPickOrder.objects.all()
    tournamentList : list = list()
    for res in queryListTournament:
        if not(res in tournamentList):
            tournamentList.append(res.tournament)

    if not(tournament in tournamentList):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    
    draftQuery = DraftPickOrder.objects.filter(tournament__exact=tournament)
    serializer = DraftPickOrderSerializer(draftQuery, context={"request": request}, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def getDraftChampion(request, championName, patch):
    # Checking if patch is correct
    queryListPatch = GameMetadata.objects.all()
    patchList : list = list()

    for res in queryListPatch:
        tempPatch = res.patch.split(".")[0] + "." + res.patch.split(".")[1]
        patchList.append(tempPatch)
    
    dfPatch = pd.DataFrame({"patch": patchList})
    dfPatchUnique = dfPatch["patch"].unique()

    if not(patch in dfPatchUnique.tolist()):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # Checking if championName is correct
    if not(championName in list(get_champion_mapping_key_reversed().keys())):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    draftQuery = DraftPickOrder.objects.filter(
        Q(bp1=championName) |
        Q(bp2=championName) |
        Q(bp3=championName) |
        Q(bp4=championName) |
        Q(bp5=championName) |
        Q(rp1=championName) |
        Q(rp2=championName) |
        Q(rp3=championName) |
        Q(rp4=championName) |
        Q(rp5=championName),
        patch__contains=patch
    )
    serializer = DraftPickOrderSerializer(draftQuery, context={"request": request}, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def getTeamNames(request, seriesId, gameNumber):
    wantedDraft = DraftPickOrder.objects.get(seriesId__exact=seriesId, gameNumner__exact=gameNumber)
    return Response([wantedDraft.teamBlue, wantedDraft.teamRed])

@api_view(['DELETE'])
def deleteAllDrafts(request):
    queryDrafPickOrder = DraftPickOrder.objects.all()
    for res in queryDrafPickOrder:
        res.delete()

    queryPlayerPicks = DraftPlayerPick.objects.all()
    for res in queryPlayerPicks:
        res.delete()

    return Response(status=status.HTTP_200_OK)

@api_view(['PATCH'])
def updateChampionDraftStats(request):

    tournamentList : list = list()
    response = requests.get(API_URL + 'api/dataAnalysis/tournament/getList')
    for tournament in response.json():
        tournamentList.append(tournament)
    
    
    for tournament in tournamentList:
        # Getting the list of patches where the tournament was played
        assosiatedPatchList : list = list()

        queryDraftPickOrder = DraftPickOrder.objects.filter(tournament__exact=tournament)
        for draftPickOrder in queryDraftPickOrder:
            if not(draftPickOrder.patch in assosiatedPatchList):
                assosiatedPatchList.append(draftPickOrder.patch)
        
        for patch in assosiatedPatchList:
            # Getting the list of champions played in a given tournament on a given patch
            associatedChampionList : list = list()
        
            queryDraftPlayerPicks = DraftPlayerPick.objects.filter(tournament__exact=tournament, patch__exact=patch)
            for draftPlayerPicks in queryDraftPlayerPicks:
                if not(draftPlayerPicks.championName in associatedChampionList):
                    associatedChampionList.append(draftPlayerPicks.championName)
            
            for championName in associatedChampionList:
                for side in ["Blue", "Red"]:
                    print("Saving stats of {} during {} at {} in {} side".format(championName, tournament, patch, side))
                    winRate : float = getChampionWinRate(championName, tournament, patch, side)
                    pickRate, pickRate1Rota, pickRate2Rota = getPickRateInfo(championName, tournament, patch, side)
                    banRate, banRate1Rota, banRate2Rota = getBanRateInfo(championName, tournament, patch, side)
                    mostPopularPickOrder : int = getMostPopularPickPosition(championName, tournament, patch, side)
                    blindPick : float = getBlindPick(championName, tournament, patch, side)
                    
                    path : str = DATA_PATH + "drafts/champion_draft_stats.csv"
                    new : bool = not(os.path.exists(path))
                    saveChampionDraftStatsCSV(path,
                                              new,
                                              championName,
                                              patch,
                                              tournament,
                                              side,
                                              winRate,
                                              pickRate,
                                              pickRate1Rota,
                                              pickRate2Rota,
                                              banRate,
                                              banRate1Rota,
                                              banRate2Rota,
                                              mostPopularPickOrder,
                                              blindPick)

        
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def getChampionDraftStats(request, patch, side, tournament):
    queryDraftPickOrder = DraftPickOrder.objects.filter(tournament__exact=tournament)
    availablePatchList : list = list()
    for res in queryDraftPickOrder:
        tempPatch = res.patch.split(".")[0] + "." + res.patch.split(".")[1]
        if not(tempPatch in availablePatchList):
            availablePatchList.append(tempPatch)
    
    if not(patch in availablePatchList):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    print(side)

    if side in ["Blue", "Red"]:
        queryChampionDraftStats = ChampionDraftStats.objects.filter(patch__contains=patch, side__exact=side, tournament__exact=tournament).order_by("championName")
        seriliazer = ChampionDraftStatsSerializer(queryChampionDraftStats, context={"request": request}, many=True)
        
        return Response(seriliazer.data)
    
    return Response(status=status.HTTP_200_OK)