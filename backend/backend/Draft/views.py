from django.shortcuts import render
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import DraftPickOrder, DraftPlayerPick, ChampionDraftStats
from .serializer import DraftPickOrderSerializer, ChampionDraftStatsSerializer, ChampionPoolSerializer


from dataAnalysis.packages.api_calls.GRID.api_calls import get_tournament_from_seriesId
from dataAnalysis.packages.api_calls.DDragon.api_calls import get_champion_mapping_key_reversed
from dataAnalysis.packages.utils_stuff.utils_func import getData
from dataAnalysis.globals import DATA_PATH, API_URL, DATE_LIMIT
from dataAnalysis.models import GameMetadata
from dataAnalysis.serializer import GameMetadataSerializer

from .packages.utils import isDraftDownloaded, isTournamentOngoing
from .packages.championStats_utils import *
from .packages.playerStats_utils import *

from .utils import import_draft, import_draftStats, import_championPools, fuseQueriesChampionDraftStats


import pandas as pd
import requests
import os
import re
from tqdm import tqdm
import time as t_time
from datetime import datetime

@api_view(['POST'])
def saveDrafts(request):
    # for idx, row in tqdm(data_metadata.iterrows(), total=data_metadata.shape[0]):
    queryAllGames = GameMetadata.objects.all()

    for game in tqdm(queryAllGames):
    # for game in queryAllGames:
        data_base_exists : bool = os.path.exists(DATA_PATH + "drafts/draft_pick_order.csv") and os.path.exists(DATA_PATH + "drafts/draft_player_picks.csv")
        file_name : str = game.name
        gameNumber : int = int(file_name.split("_")[2][0])
        seriesId : int = game.seriesId
        
        
        # Saving the draft into our CSV database

        # Checking if the database exists
        if data_base_exists:
            # Checking if the draft we want to save is already in our database
            if not(isDraftDownloaded(seriesId, gameNumber)):
                (data, _, _, _) = getData(seriesId, gameNumber)
                if len(data.draftSnapshotList) > 0:
                    date = game.date
                    # Saving the draft into our csv database
                    patch : str = game.patch
                    tournament : str = get_tournament_from_seriesId(seriesId)
                    teamBlue = game.teamBlue
                    teamRed = game.teamRed
                    # print(seriesId, "new game")
                    data.draftToCSV(DATA_PATH + "drafts/", new=False, patch=patch, seriesId=seriesId, tournament=tournament, gameNumber=gameNumber, date=date, teamBlue=teamBlue, teamRed=teamRed)
                # else:
                #     print("Draft not accessible")
            # else:
            #     print("Game of seriesId {} n°{} already in databae".format(seriesId, gameNumber))
        else:
            (data, _, _, _) = getData(seriesId, gameNumber)
            if len(data.draftSnapshotList) > 0:
                date = game.date
                patch : str = game.patch
                tournament : str = get_tournament_from_seriesId(seriesId)
                teamBlue = game.teamBlue
                teamRed = game.teamRed
                # print(seriesId)
                data.draftToCSV(DATA_PATH + "drafts/", new=True, patch=patch, seriesId=seriesId, tournament=tournament, gameNumber=gameNumber, date=date, teamBlue=teamBlue, teamRed=teamRed)
            # else:
            #     print("Draft not accessible")

    import_draft()


    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def getLatestDraft(request, limit, scrimStr):
    scrim : int = int(scrimStr)
    if not(scrim == 0 or scrim == 1):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if scrim == 0:
        draftQuery = DraftPickOrder.objects.filter(tournament__exact="League of Legends Scrims").order_by("-date")[:limit]
        serializer = DraftPickOrderSerializer(draftQuery, context={"request": request}, many=True)
    else:
        draftQuery = DraftPickOrder.objects.filter(~Q(tournament="League of Legends Scrims")).order_by("-date")[:limit]
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
    
    
    if tournament == "League of Legends Scrims":
        draftQuery = DraftPickOrder.objects.filter(tournament__exact=tournament, date__gte=DATE_LIMIT)
    else:
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
def updateChampionDraftStats(request, tournamentListStr : str):
    
    if len(tournamentListStr) == 0:

        tournamentList : list = list()
        response = requests.get(API_URL + 'api/dataAnalysis/tournament/getList')


        for tournament in response.json():
            formated_tournament : str = re.sub(r'\([^)]*\)', '', tournament)
            
            if tournament != "League of Legends Scrims":
                if not(isTournamentOngoing(formated_tournament[:-1])):
                    tournamentList.append(tournament)
            else:
                tournamentList.append(tournament)

    else:
        tournamentList : list = tournamentListStr.split(",")
    
    
    for tournament in tournamentList:
        print(tournament)
        # Getting the list of patches where the tournament was played
        assosiatedPatchList : list = list()

        queryDraftPickOrder = DraftPickOrder.objects.filter(tournament__exact=tournament)
        for draftPickOrder in queryDraftPickOrder:
            tempPatch = draftPickOrder.patch.split(".")[0] + "." + draftPickOrder.patch.split(".")[1]
            if not(tempPatch in assosiatedPatchList):
                assosiatedPatchList.append(tempPatch)

        if tournament == "League of Legends Scrims":
            assosiatedPatchList = [assosiatedPatchList[-1]]
        
        
        # if os.path.exists(DATA_PATH + "draft/champion_draft_stats.csv"):
        #     os.remove(DATA_PATH + "draft/champion_draft_stats.csv")

        for patch in assosiatedPatchList:
            print("\t{}".format(patch))
            # Getting the list of champions played in a given tournament on a given patch
            associatedChampionList : list = list()
        
            queryDraftPlayerPicks = DraftPlayerPick.objects.filter(tournament__exact=tournament, patch__contains=patch)
            for draftPlayerPicks in queryDraftPlayerPicks:
                if not(draftPlayerPicks.championName in associatedChampionList):
                    associatedChampionList.append(draftPlayerPicks.championName)
            
            for championName in tqdm(associatedChampionList):
            # for championName in associatedChampionList:
                for side in ["Blue", "Red"]:
                    if isChampionPicked(championName, tournament, patch, side):
                        # print("Saving stats of {} during {} at {} in {} side".format(championName, tournament, patch, side), end="\n")

                        winRate : float = getChampionWinRate(championName, tournament, patch, side)
                        pickRate, pickRate1Rota, pickRate2Rota = getPickRateInfo(championName, tournament, patch, side)
                        banRate, banRate1Rota, banRate2Rota = getBanRateInfo(championName, tournament, patch, side)
                        mostPopularPickOrder : int = getMostPopularPickPosition(championName, tournament, patch, side)
                        blindPick : float = getBlindPick(championName, tournament, patch, side)
                        mostPopularRole : str = getMostPopularRole(championName, tournament, patch, side)                
                        
                        
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
                                                blindPick,
                                                mostPopularRole)
    
    import_draftStats()
    return Response(status=status.HTTP_200_OK)

@api_view(['DELETE'])
def deleteAllChampionDraftStats(request):
    queryChampionDraftStats = ChampionDraftStats.objects.all()
    for res in queryChampionDraftStats:
        res.delete()

    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def getChampionDraftStats(request, patch, side, tournament):
    if tournament == "League of Legends Scrims":
        queryDraftPickOrder = DraftPickOrder.objects.filter(tournament__exact=tournament, date__gte=DATE_LIMIT)
    else:
        queryDraftPickOrder = DraftPickOrder.objects.filter(tournament__exact=tournament)
    availablePatchList : list = list()
    for res in queryDraftPickOrder:
        tempPatch = res.patch.split(".")[0] + "." + res.patch.split(".")[1]
        if not(tempPatch in availablePatchList):
            availablePatchList.append(tempPatch)
    
    if not(patch in availablePatchList):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if side in ["Blue", "Red"]:
        
        queryChampionDraftStats = ChampionDraftStats.objects.filter(patch__contains=patch, side__exact=side, tournament__exact=tournament).order_by("championName")
        serializer = ChampionDraftStatsSerializer(queryChampionDraftStats, context={"request": request}, many=True)
        
        return Response(serializer.data)

    else:
        queryBlue = ChampionDraftStats.objects.filter(tournament__exact=tournament, patch__contains=patch, side__exact="Blue")
        queryRed = ChampionDraftStats.objects.filter(tournament__exact=tournament, patch__contains=patch, side__exact="Red")
        
        return Response(fuseQueriesChampionDraftStats(queryRed, queryBlue))
    

def lowercase_first_letter(s : str):
    if not s:
        return s
    return s[0].lower() + s[1:]

@api_view(['GET'])
def getTopChampions(request, role, filter, patch, side, tournament):
    if side != "Both":
        if tournament == "League of Legends Scrims":
            query = ChampionDraftStats.objects.filter(mostPopularRole__exact=role, tournament__exact=tournament, patch__contains=patch, side__exact=side,  date__gte=DATE_LIMIT)
        else:
            query = ChampionDraftStats.objects.filter(mostPopularRole__exact=role, tournament__exact=tournament, patch__contains=patch, side__exact=side)

        if filter == "WinRate":
            queryFiltered = query.order_by("-winRate")
        elif filter == "PickRate":
            queryFiltered = query.order_by("-globalPickRate")
        elif filter == "BanRate":
            queryFiltered = query.order_by("-globalBanRate")
        
        
        serializer = ChampionDraftStatsSerializer(queryFiltered, context={"request": request}, many=True)
        return Response(serializer.data)

    elif side == "Both":
        if tournament == "League of Legends Scrims":
            queryBlue = ChampionDraftStats.objects.filter(mostPopularRole__exact=role, tournament__exact=tournament, patch__contains=patch, side__exact="Blue",  date__gte=DATE_LIMIT)
            queryRed = ChampionDraftStats.objects.filter(mostPopularRole__exact=role, tournament__exact=tournament, patch__contains=patch, side__exact="Red",  date__gte=DATE_LIMIT)

            res : dict = fuseQueriesChampionDraftStats(queryRed, queryBlue)
            
            if filter == "PickRate":
                return Response(sorted(res, key=lambda d:-d["globalPickRate"]))
            elif filter == "BanRate":
                return Response(sorted(res, key=lambda d:-d["globalBanRate"]))
            elif filter == "WinRate":
                return Response(sorted(res, key=lambda d:-d["winRate"]))  
        else:
            queryBlue = ChampionDraftStats.objects.filter(mostPopularRole__exact=role, tournament__exact=tournament, patch__contains=patch, side__exact="Blue")
            queryRed = ChampionDraftStats.objects.filter(mostPopularRole__exact=role, tournament__exact=tournament, patch__contains=patch, side__exact="Red")

            res : dict = fuseQueriesChampionDraftStats(queryRed, queryBlue)

            if filter == "PickRate":
                return Response(sorted(res, key=lambda d:-d["globalPickRate"]))
            elif filter == "BanRate":
                return Response(sorted(res, key=lambda d:-d["globalBanRate"]))
            elif filter == "WinRate":
                return Response(sorted(res, key=lambda d:-d["winRate"]))    
        

@api_view(['PATCH'])
def updatePlayerStats(request, tournamentListStr):
    # Getting the list of tournament
    if len(tournamentListStr) == 0:

        tournamentList : list = list()
        response = requests.get(API_URL + 'api/dataAnalysis/tournament/getList')


        for tournament in response.json():
            formated_tournament : str = re.sub(r'\([^)]*\)', '', tournament)
            
            if tournament != "League of Legends Scrims":
                if not(isTournamentOngoing(formated_tournament[:-1])):
                    tournamentList.append(tournament)
            else:
                tournamentList.append(tournament)

    else:
        tournamentList : list = tournamentListStr.split(",")


    for tournament in tournamentList:
        print(tournament)
        associatedPlayerList : list = list()
        if tournament == "League of Legends Scrims":
            queryPlayer = DraftPlayerPick.objects.filter(tournament__exact=tournament, date__gte=DATE_LIMIT)
        else:
            queryPlayer = DraftPlayerPick.objects.filter(tournament__exact=tournament)
        
        for res in queryPlayer:
            if not(res.sumonnerName in associatedPlayerList):
                associatedPlayerList.append(res.sumonnerName)

        for playerName in associatedPlayerList:
            print("\t{}".format(playerName))
            associatedChampionList : list = list()
            if tournament == "League of Legends Scrims":
                queryChampion = DraftPlayerPick.objects.filter(tournament__exact=tournament, sumonnerName__exact=playerName, date__gte=DATE_LIMIT)
            else:
                queryChampion = DraftPlayerPick.objects.filter(tournament__exact=tournament, sumonnerName__exact=playerName)
            
            for res in queryChampion:
                if not(res.championName in associatedChampionList):
                    associatedChampionList.append(res.championName)

            for championName in tqdm(associatedChampionList):
                
                globalPickRate = getPlayerChampionPickRate(playerName, championName, tournament)
                globalWinRate = getPlayerChampionWinRate(playerName, championName, tournament)
                nbGames = getPlayerChampionNbGames(playerName, championName, tournament)
                kda = getPlayerChampionKDA(playerName, championName, tournament)
                
                path : str = DATA_PATH + "drafts/player_championPool.csv"
                new : bool = not(os.path.exists(path))
                saveChampionPoolCSV(
                    path,
                    new,
                    playerName,
                    championName,
                    tournament,
                    globalPickRate,
                    globalWinRate,
                    nbGames,
                    kda
                )
    # import_championPools()
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def getPlayerStats(request, summonnerName, tournament, filter):
    print(ChampionPool.objects.all().count())
    
    query = ChampionPool.objects.filter(summonnerName__exact=summonnerName, tournament__exact=tournament)
    
    if filter == "pickRate":
        res = query.order_by("-globalPickRate")
    elif filter == "winRate":
        res = query.order_by("-winRate")
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return_data = ChampionPoolSerializer(res, context={"request": request}, many=True)
    
    return Response(return_data.data)

@api_view(['DELETE'])
def deleteAllChampionPool(request):
    query = ChampionPool.objects.all()

    for res in query:
        res.delete()

    return Response(status=status.HTTP_200_OK)

@api_view(["GET"])
def getDraftGame(request, seriesId : int, gameNumber : int):
    query = DraftPickOrder.objects.filter(seriesId__exact=seriesId, gameNumner__exact=gameNumber)
    serializer = DraftPickOrderSerializer(query, context={"request": request}, many=True)

    return Response(serializer.data)