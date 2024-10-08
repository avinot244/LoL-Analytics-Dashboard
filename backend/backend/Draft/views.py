from django.shortcuts import render
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import DraftPickOrder, DraftPlayerPick, ChampionDraftStats, ChampionBanStats
from .serializer import DraftPickOrderSerializer, ChampionDraftStatsSerializer, ChampionPoolSerializer, ChampionBanStatsSerializer


from dataAnalysis.packages.api_calls.GRID.api_calls import get_tournament_from_seriesId
from dataAnalysis.packages.api_calls.DDragon.api_calls import get_champion_mapping_key_reversed
from dataAnalysis.packages.utils_stuff.utils_func import getData
from dataAnalysis.globals import DATA_PATH, API_URL, DATE_LIMIT
from dataAnalysis.models import GameMetadata
from dataAnalysis.serializer import GameMetadataSerializer

from .packages.utils import isDraftDownloaded, isTournamentOngoing
import Draft.packages.championStats_utils as ChampionPicksStats
import Draft.packages.championBans_utils as ChampionBansStats
from .packages.playerStats_utils import *

from .utils import import_draft, import_draftStats, delete_draftStats, delete_banStats, import_banStats, fuseQueriesChampionDraftStats, fuseQueriesChampionBansStats


import pandas as pd
import requests
import os
import re
from tqdm import tqdm

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
    if not(championName in list(get_champion_mapping_key_reversed(patch + ".1").keys())):
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
    for res in tqdm(queryDrafPickOrder):
        res.delete()

    queryPlayerPicks = DraftPlayerPick.objects.all()
    for res in tqdm(queryPlayerPicks):
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

        for patch in assosiatedPatchList:
            print("\t{}".format(patch))
            # Getting the list of champions played in a given tournament on a given patch
            associatedChampionList : list = list()
        
            queryDraftPickOrder = DraftPickOrder.objects.filter(tournament__exact=tournament, patch__contains=patch)
            for draftPickOrder in queryDraftPickOrder:
                if not(draftPickOrder.bp1 in associatedChampionList):
                    associatedChampionList.append(draftPickOrder.bp1)
                if not(draftPickOrder.bp2 in associatedChampionList):
                    associatedChampionList.append(draftPickOrder.bp2)
                if not(draftPickOrder.bp3 in associatedChampionList):
                    associatedChampionList.append(draftPickOrder.bp3)
                if not(draftPickOrder.bp4 in associatedChampionList):
                    associatedChampionList.append(draftPickOrder.bp4)
                if not(draftPickOrder.bp5 in associatedChampionList):
                    associatedChampionList.append(draftPickOrder.bp5)
                
                if not(draftPickOrder.bb1 in associatedChampionList):
                    associatedChampionList.append(draftPickOrder.bb1)
                if not(draftPickOrder.bb2 in associatedChampionList):
                    associatedChampionList.append(draftPickOrder.bb2)
                if not(draftPickOrder.bb3 in associatedChampionList):
                    associatedChampionList.append(draftPickOrder.bb3)
                if not(draftPickOrder.bb4 in associatedChampionList):
                    associatedChampionList.append(draftPickOrder.bb4)
                if not(draftPickOrder.bb5 in associatedChampionList):
                    associatedChampionList.append(draftPickOrder.bb5)
                
                
                if not(draftPickOrder.rp1 in associatedChampionList):
                    associatedChampionList.append(draftPickOrder.rp1)
                if not(draftPickOrder.rp2 in associatedChampionList):
                    associatedChampionList.append(draftPickOrder.rp2)
                if not(draftPickOrder.rp3 in associatedChampionList):
                    associatedChampionList.append(draftPickOrder.rp3)
                if not(draftPickOrder.rp4 in associatedChampionList):
                    associatedChampionList.append(draftPickOrder.rp4)
                if not(draftPickOrder.rp5 in associatedChampionList):
                    associatedChampionList.append(draftPickOrder.rp5)
                
                if not(draftPickOrder.rb1 in associatedChampionList):
                    associatedChampionList.append(draftPickOrder.rb1)
                if not(draftPickOrder.rb2 in associatedChampionList):
                    associatedChampionList.append(draftPickOrder.rb2)
                if not(draftPickOrder.rb3 in associatedChampionList):
                    associatedChampionList.append(draftPickOrder.rb3)
                if not(draftPickOrder.rb4 in associatedChampionList):
                    associatedChampionList.append(draftPickOrder.rb4)
                if not(draftPickOrder.rb5 in associatedChampionList):
                    associatedChampionList.append(draftPickOrder.rb5)
            
            for championName in tqdm(associatedChampionList):
            # for championName in associatedChampionList:
                for side in ["Blue", "Red"]:
                    # print("Checkin stats of {} during {} at {} in {} side".format(championName, tournament, patch, side), end="\n")
                    if ChampionPicksStats.isChampionPicked(championName, tournament, patch, side):
                        # print("Saving stats of {} during {} at {} in {} side".format(championName, tournament, patch, side), end="\n")

                        winRate : float = ChampionPicksStats.getChampionWinRate(championName, tournament, patch, side)
                        pickRate, pickRate1Rota, pickRate2Rota = ChampionPicksStats.getPickRateInfo(championName, tournament, patch, side)
                        banRate, banRate1Rota, banRate2Rota = ChampionPicksStats.getBanRateInfo(championName, tournament, patch, side)
                        mostPopularPickOrder : int = ChampionPicksStats.getMostPopularPickPosition(championName, tournament, patch, side)
                        blindPick : float = ChampionPicksStats.getBlindPick(championName, tournament, patch, side)
                        mostPopularRole : str = ChampionPicksStats.getMostPopularRole(championName, tournament, patch, side)
                        draftPresence : float = (pickRate + banRate)/2
                        
                        path : str = DATA_PATH + "drafts/champion_draft_stats.csv"
                        new : bool = not(os.path.exists(path))
                        ChampionPicksStats.saveChampionDraftStatsCSV(
                            path,
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
                            draftPresence,
                            mostPopularPickOrder,
                            blindPick,
                            mostPopularRole
                        )
                    elif ChampionBansStats.isChampionBanned(championName, tournament, patch, side):
                        banRate, banRate1Rota, banRate2Rota = ChampionBansStats.getBanRateInfo(championName, tournament, patch, side)
                        
                        path : str = DATA_PATH + "drafts/champion_bans_stats.csv"
                        new : bool = not(os.path.exists(path))
                        ChampionBansStats.saveChampionBanStatsCSV(
                            path,
                            new,
                            championName,
                            patch,
                            tournament,
                            side,
                            banRate,
                            banRate1Rota,
                            banRate2Rota
                        )
    
    delete_draftStats()
    delete_banStats()
    import_draftStats()
    import_banStats()
    return Response(status=status.HTTP_200_OK)

@api_view(['DELETE'])
def deleteAllChampionDraftStats(request):
    queryChampionDraftStats = ChampionDraftStats.objects.all()
    for res in tqdm(queryChampionDraftStats):
        res.delete()

    return Response(status=status.HTTP_200_OK)

@api_view(['DELETE'])
def deleteAllChampionBansStats(request):
    queryChampionDraftStats = ChampionBanStats.objects.all()
    for res in tqdm(queryChampionDraftStats):
        res.delete()

    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
def deleteDraftStatSingleGame(request, seriesId : int, gameNumber : int):
    # 2682736
    queryDraftPlayerPicks = DraftPlayerPick.objects.filter(seriesId__exact=seriesId, gameNumber__exact=gameNumber)
    for res in queryDraftPlayerPicks:
        res.delete()

    queryDraftPickOrder = DraftPickOrder.objects.filter(seriesId__exact=seriesId, gameNumner__exact=gameNumber)
    for res in queryDraftPickOrder:
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
    

@api_view(['GET'])
def getChampionDraftBans(request, patch : str, side : str, tournament : str):
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
        queryChampionDraftBans = ChampionBanStats.objects.filter(patch__contains=patch, side__exact=side, tournament__exact=tournament).order_by("championName")
        serializer = ChampionBanStatsSerializer(queryChampionDraftBans, context={"request": request}, many=True)
        return Response(serializer.data)
    else:
        queryBlue = ChampionBanStats.objects.filter(tournament__exact=tournament, patch__contains=patch, side__exact="Blue")
        queryRed = ChampionBanStats.objects.filter(tournament__exact=tournament, patch__contains=patch, side__exact="Red")
        return Response(fuseQueriesChampionBansStats(queryRed, queryBlue))        

def lowercase_first_letter(s : str):
    if not s:
        return s
    return s[0].lower() + s[1:]

@api_view(['GET'])
def getTopChampions(request, role, filter, patch, side, tournament):
    if side != "Both":
        # if tournament == "League of Legends Scrims":
        #     query = ChampionDraftStats.objects.filter(mostPopularRole__exact=role, tournament__exact=tournament, patch__contains=patch, side__exact=side,  date__gte=DATE_LIMIT)
        # else:
        # TODO : Get list of championDraftStats where associated patch is linked to a date gte than DATE_LIMIT
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
            queryBlue = ChampionDraftStats.objects.filter(mostPopularRole__exact=role, tournament__exact=tournament, patch__contains=patch, side__exact="Blue")
            queryRed = ChampionDraftStats.objects.filter(mostPopularRole__exact=role, tournament__exact=tournament, patch__contains=patch, side__exact="Red")

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
            # for championName in associatedChampionList:
                globalPickRate = getPlayerChampionPickRate(playerName, championName, tournament)
                globalWinRate = getPlayerChampionWinRate(playerName, championName, tournament)
                nbGames = getPlayerChampionNbGames(playerName, championName, tournament)
                kda = getPlayerChampionKDA(playerName, championName, tournament)
                
                path : str = DATA_PATH + "drafts/player_championPool.csv"
                new : bool = not(os.path.exists(path))
                # print("{}-{} : {}% PR, {}% WR, {} games, {} KDA".format(playerName, championName, globalPickRate, globalWinRate, nbGames, kda))
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

    for res in tqdm(query):
        res.delete()

    return Response(status=status.HTTP_200_OK)

@api_view(["GET"])
def getDraftGame(request, seriesId : int, gameNumber : int):
    query = DraftPickOrder.objects.filter(seriesId__exact=seriesId, gameNumner__exact=gameNumber)
    serializer = DraftPickOrderSerializer(query, context={"request": request}, many=True)

    return Response(serializer.data)