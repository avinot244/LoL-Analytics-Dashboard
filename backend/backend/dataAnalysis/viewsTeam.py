import json
from tqdm import tqdm
import requests
import numpy as np
import matplotlib.pyplot as plt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

from .packages.Parsers.Separated.Game.SeparatedData import SeparatedData
from .packages.Parsers.Separated.Game.Snapshot import Snapshot
from .models import GameMetadata
from .globals import SIDES, ROLE_LIST, API_URL, DATE_LIMIT
from .packages.utils_stuff.utils_func import getData
from .request_models import PlayerPositionRequest, WardPlacedRequest, WardPlacedGlobalRequest, GameTimeFrameRequest, TeamStatsRequest, GetGameRequest, TeamSideRequest, PlayerPositionGlobalRequest, TeamDraftDataRequest, TournamentListRequest
from .packages.Parsers.Separated.Game.getters import getResetTriggers, getWardTriggers, getPlayerPositionHistoryTimeFramed, getKillTriggers, getTPTriggers
from .packages.Parsers.Separated.Events.EventTypes import ChannelingEndedEvent
from .packages.utils_stuff.utils_func import convertTime
from .packages.AreaMapping.Zone import Zone
from .packages.AreaMapping.Grid import Grid
from .packages.utils_stuff.globals import entireBotLaneBoundary, entireTopLaneBoundary
from .packages.utils_stuff.Position import Position

from Draft.utils import fuseDataChampionsDraftStats
from Draft.serializer import ChampionDraftStatsSerializer, DraftPlayerPick
from Draft.models import ChampionDraftStats



@api_view(['GET'])
def getTeamList(request):
    teamList : list[str] = list()
    allData = GameMetadata.objects.all()
    for gameMetadataobject in allData:
        if not(gameMetadataobject.teamBlue in teamList):
            teamList.append(gameMetadataobject.teamBlue)
        elif not(gameMetadataobject.teamRed in teamList):
            teamList.append(gameMetadataobject.teamRed)
    return Response(teamList)

@api_view(['GET'])
def getTournamentsFromTeam(request, team : str):
    tournamentList : list[str] = list()
    allData = GameMetadata.objects.filter(Q(teamRed=team) | Q(teamBlue=team))
    for gameMetadataObject in allData:
        if not(gameMetadataObject.tournament in tournamentList):
            tournamentList.append(gameMetadataObject.tournament)
    return Response(tournamentList)

@api_view(['PATCH'])
def getGames(request):
    o : GetGameRequest = GetGameRequest(**json.loads(request.body))
    gameList : list[str] = list()
    allData = GameMetadata.objects.filter(Q(teamRed=o.team) | Q(teamBlue=o.team), tournament__in=o.tournaments)
    for gameMetadata in allData:
        temp_dict : dict = dict()
        game_str = "{} {} vs {} Game {} {}".format(gameMetadata.tournament, gameMetadata.teamBlue, gameMetadata.teamRed, gameMetadata.gameNumber, gameMetadata.date)
        temp_dict["str"] = game_str
        temp_dict["seriesId"] = gameMetadata.seriesId
        temp_dict["gameNumber"] = gameMetadata.gameNumber
        temp_dict["tournament"] = gameMetadata.tournament
        
        gameList.append(temp_dict)
        
    return Response(gameList)

@api_view(['PATCH'])
def getPlayerPosition(request):
    o : PlayerPositionRequest = PlayerPositionRequest(**json.loads(request.body))
    (data, gameDuration, _, _) = getData(int(o.seriesId), o.gameNumber)
    
    participantID = data.gameSnapshotList[0].teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)].participantID
    
    # get participant ID from o.side and o.role
    playerPosition = getPlayerPositionHistoryTimeFramed(data, gameDuration, participantID, o.begTime, o.endTime)
    
    # Building the response
    res : list[list] = [pos.toList() for pos in playerPosition]
    
    return Response(res)

@api_view(['PATCH'])
def getPlayerPositionGlobal(request):
    o : PlayerPositionGlobalRequest = PlayerPositionGlobalRequest(**json.loads(request.body))
    result : list[dict] = list()
    
    metadataList = GameMetadata.objects.filter(Q(teamRed=o.team) | Q(teamBlue=o.team), tournament__in=o.tournamentList)
    
    for gameMetadata in tqdm(metadataList):
        data : SeparatedData
        (data, gameDuration, _, _) = getData(int(gameMetadata.seriesId), gameMetadata.gameNumber)
    
        participantID = data.gameSnapshotList[0].teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)].participantID
        
        # get participant ID from o.side and o.role
        playerPosition = getPlayerPositionHistoryTimeFramed(data, gameDuration, participantID, o.begTime, o.endTime)
        
        # Building the response
        res : list[list] = [pos.toList() for pos in playerPosition]
        
        result += res
    
    return Response(result)
@api_view(['PATCH'])
def getPlayerResetPositions(request):
    o : PlayerPositionRequest = PlayerPositionRequest(**json.loads(request.body))
    (data, gameDuration, _, endGameTime) = getData(int(o.seriesId), o.gameNumber)
    
    participantID = data.gameSnapshotList[0].teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)].participantID
    playerName = data.gameSnapshotList[0].teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)].playerName
    
    team : str = ""
    if data.gameSnapshotList[0].teams[0].isPlayerInTeam(participantID):
        team = "blueTeam"
    elif data.gameSnapshotList[0].teams[1].isPlayerInTeam(participantID):
        team = "redTeam"
    
    resetTriggers = getResetTriggers(data, gameDuration, endGameTime, o.begTime, o.endTime)[team][playerName]
    
    # Building the response
    res : list[list] = [(d["position"]["x"], d["position"]["y"]) for d in resetTriggers]
    
    return Response(res)

@api_view(['PATCH'])
def getPlayerResetPositionsGlobal(request):
    o : PlayerPositionGlobalRequest = PlayerPositionGlobalRequest(**json.loads(request.body))
    result : list[dict] = list()
    
    metadataList = GameMetadata.objects.filter(Q(teamRed=o.team) | Q(teamBlue=o.team), tournament__in=o.tournamentList)
    for gameMetadata in tqdm(metadataList):
        data : SeparatedData
        (data,_ , _, endGameTime) = getData(int(gameMetadata.seriesId), gameMetadata.gameNumber)
        participantID = data.gameSnapshotList[0].teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)].participantID
        playerName = data.gameSnapshotList[0].teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)].playerName
        
        team : str = ""
        if data.gameSnapshotList[0].teams[0].isPlayerInTeam(participantID):
            team = "blueTeam"
        elif data.gameSnapshotList[0].teams[1].isPlayerInTeam(participantID):
            team = "redTeam"
        
        resetTriggers = getResetTriggers(data, gameMetadata.gameDuration, endGameTime, o.begTime, o.endTime, verbose=False)[team][playerName]
        result += [(d["position"]["x"], d["position"]["y"]) for d in resetTriggers]
        
    return Response(result)   

@api_view(['PATCH'])
def getWardPlacedPositions(request):
    o : WardPlacedRequest = WardPlacedRequest(**json.loads(request.body))
    (data, gameDuration, _, endGameTime) = getData(int(o.seriesId), o.gameNumber)
    
    participantID = data.gameSnapshotList[0].teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)].participantID
    playerName = data.gameSnapshotList[0].teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)].playerName
    
    team : str = ""
    if data.gameSnapshotList[0].teams[0].isPlayerInTeam(participantID):
        team = "blueTeam"
    elif data.gameSnapshotList[0].teams[1].isPlayerInTeam(participantID):
        team = "redTeam"
    
    wardTriggers = getWardTriggers(data, gameDuration, endGameTime, o.begTime, o.endTime, o.wardTypes)[team][playerName]
    
    # Building the response
    res : list[list] = [(d["position"]["x"], d["position"]["z"]) for d in wardTriggers]
    
    return Response(res)

@api_view(['PATCH'])
def getWardPlacedPositionsGlobal(request):
    o : WardPlacedGlobalRequest = WardPlacedGlobalRequest(**json.loads(request.body))
    result : list[dict] = list()
    
    metadataList = GameMetadata.objects.filter(Q(teamRed=o.team) | Q(teamBlue=o.team), tournament__in=o.tournamentList)
    for gameMetadata in tqdm(metadataList):
        data : SeparatedData
        (data, gameDuration, _, endGameTime) = getData(int(gameMetadata.seriesId), gameMetadata.gameNumber)
        
        participantID = data.gameSnapshotList[0].teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)].participantID
        playerName = data.gameSnapshotList[0].teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)].playerName
        
        team : str = ""
        if data.gameSnapshotList[0].teams[0].isPlayerInTeam(participantID):
            team = "blueTeam"
        elif data.gameSnapshotList[0].teams[1].isPlayerInTeam(participantID):
            team = "redTeam"
        
        wardTriggers = getWardTriggers(data, gameDuration, endGameTime, o.begTime, o.endTime, o.wardTypes)[team][playerName]
        result += [(d["position"]["x"], d["position"]["z"]) for d in wardTriggers]
    return Response(result)

@api_view(['PATCH'])
def getKillEvents(request):
    o : GameTimeFrameRequest = GameTimeFrameRequest(**json.loads(request.body))
    (data, gameDuration, _, endGameTime) = getData(int(o.seriesId), o.gameNumber)

    killEvents = getKillTriggers(data, gameDuration, endGameTime, o.begTime, o.endTime)[o.team]
    
    return Response(killEvents)

@api_view(['PATCH'])
def getGrubsDrakeStats(request):
    o : TeamStatsRequest = TeamStatsRequest(**json.loads(request.body))
    
    if len(o.tournamentList) == 0:
        allObjectsBlueSide = GameMetadata.objects.filter(teamBlue=o.teamName)
        allObjectsRedSide = GameMetadata.objects.filter(teamRed=o.teamName)
    else:
        allObjectsBlueSide = GameMetadata.objects.filter(teamBlue=o.teamName, tournament__in=o.tournamentList)
        allObjectsRedSide = GameMetadata.objects.filter(teamRed=o.teamName, tournament__in=o.tournamentList)
    
    response : list[list] = list()
    
    for nDrake in range(0, 5):
        tempList : list = list()
        for nGrubs in range(0, 7):
            # For blue side
            blueData = allObjectsBlueSide.filter(voidGrubsBlueKills=nGrubs, dragonBlueKills=nDrake)
            nbGamesBlue : int = len(blueData)
            nbWinBlue = len(blueData.filter(winningTeam=0))
            
            # For red side
            redData = allObjectsRedSide.filter(voidGrubsRedKills=nGrubs, dragonRedKills=nDrake)
            nbGamesRed : int = len(redData)
            nbWinRed = len(redData.filter(winningTeam=1))
            
            
            if nbGamesRed + nbGamesBlue == 0:
                tempList.append({
                    "nGrubs": nGrubs,
                    "nDrake": nDrake,
                    "totalWins": nbWinBlue + nbWinRed,
                    "totalGames": nbGamesBlue + nbGamesRed,
                    "winRate": None
                })
            else:
                tempList.append({
                    "nGrubs": nGrubs,
                    "nDrake": nDrake,
                    "totalWins": nbWinBlue + nbWinRed,
                    "totalGames": nbGamesBlue + nbGamesRed,
                    "winRate": (nbWinBlue + nbWinRed)/(nbGamesBlue + nbGamesRed)
                })
        response.append(tempList)
    # We want a list of triples [nGrubs, nDrakes, winRate, nbGames]
    return Response(response)

@api_view(['PATCH'])
def getGrubsDrakeStatsGlobal(request):
    o : TournamentListRequest = TournamentListRequest(**json.loads(request.body))
    if len(o.tournamentList) == 0:
        tournamentListRequest = GameMetadata.objects.filter(date__gte=DATE_LIMIT)
        for element in tournamentListRequest:
            if not(element.tournament in o.tournamentList):
                o.tournamentList.append(element.tournament)
        # print(o.tournamentList)
        # return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # Get all the teams that played in the given tournaments
    teamList : list[str] = list()
    teamListRequest = GameMetadata.objects.filter(tournament__in=o.tournamentList)
    for element in teamListRequest:
        if not(element.teamBlue in teamList):
            teamList.append(element.teamBlue)
        if not(element.teamRed in teamList):
            teamList.append(element.teamRed)
    
    # Compute the grubs/drake heatmap for each team
    heatMapList : list[list[list[dict]]] = list()
    for teamName in teamList:
        data = requests.patch(url=f"{API_URL}api/teamAnalysis/getGrubsDrakesStats/", data=json.dumps({
            "teamName": teamName,
            "tournamentList": o.tournamentList
        }))
        heatMapList.append(data.json())
    
    # Make the average of it
    resultHeatmap = [[{"nGrubs": i, "nDrake": j, "totalWins": 0, "totalGames": 0, "winRate": 0} for i in range(7)] for j in range(5)]
    print(len(resultHeatmap))
    print(len(resultHeatmap[0]))
    for heatmapData in heatMapList:
        for heatmapData in heatMapList:
            for i in range(5):
                for j in range(7):
                    resultHeatmap[i][j]["totalWins"] += heatmapData[i][j]["totalWins"]
                    resultHeatmap[i][j]["totalGames"] += heatmapData[i][j]["totalGames"]
        
        for i in range(5):
            for j in range(7):
                if resultHeatmap[i][j]["totalGames"] > 0:
                    resultHeatmap[i][j]["winRate"] = resultHeatmap[i][j]["totalWins"] / resultHeatmap[i][j]["totalGames"]
                else:
                    resultHeatmap[i][j]["winRate"] = None
    
    

    # Create a heatmap from the resultHeatmap data
    heatmap_data = np.zeros((5, 7))
    for i in range(5):
        for j in range(7):
            if resultHeatmap[i][j]["winRate"] is not None:
                heatmap_data[i, j] = resultHeatmap[i][j]["winRate"]

    plt.figure(figsize=(10, 8))
    plt.imshow(heatmap_data, cmap='Oranges', interpolation='nearest')
    plt.colorbar(label='Win Rate')
    plt.xlabel('Number of Grubs')
    plt.ylabel('Number of Drakes')
    plt.title('Heatmap of Win Rate by Number of Grubs and Drakes')
    plt.xticks(np.arange(7), np.arange(7))
    plt.yticks(np.arange(5), np.arange(5))
    # Add text annotations for each tile
    for i in range(5):
        for j in range(7):
            totalGames = resultHeatmap[i][j]["totalGames"]
            totalWins = resultHeatmap[i][j]["totalWins"]
            totalLosses = totalGames - totalWins
            totalWinRate = resultHeatmap[i][j]["winRate"]
            if totalWinRate is not None:
                totalWinRate = f'{totalWinRate * 100:.0f}'
                text = f'W: {totalWins}\nL: {totalLosses}\nG: {totalGames}\n WR: {totalWinRate}%'
                plt.text(j, i, text, ha='center', va='center', color='black')
            else:
                plt.gca().add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, color='black'))

    plt.savefig('./databases/grubs_drakes_heatmap.png')
    plt.close()
    return Response(resultHeatmap)
    

@api_view(['PATCH'])
def getFirstTowerHeraldStats(request):
    o : TeamStatsRequest = TeamStatsRequest(**json.loads(request.body))
    if len(o.tournamentList) == 0:
        allObjectsBlueSide = GameMetadata.objects.filter(teamBlue=o.teamName, firstTower=1, heraldBlueKills__gt=0)
        allObjectsRedSide = GameMetadata.objects.filter(teamRed=o.teamName, firstTower=0, heraldRedKills__gt=0)
    else:
        allObjectsBlueSide = GameMetadata.objects.filter(teamBlue=o.teamName, tournament__in=o.tournamentList, firstTower=1, heraldBlueKills__gt=0)
        allObjectsRedSide = GameMetadata.objects.filter(teamRed=o.teamName, tournament__in=o.tournamentList, firstTower=0, heraldRedKills__gt=0)
    
    firstTowerHeraldDataBlue = allObjectsBlueSide.filter(winningTeam=0)
    firstTowerHeraldDataRed = allObjectsRedSide.filter(winningTeam=1)
    
    totalGamesBlueSide = len(allObjectsBlueSide)
    totalGamesRedSide = len(allObjectsRedSide)
    
    if totalGamesBlueSide == 0:
        if totalGamesRedSide == 0:
            return Response(-1)
        else:
            return Response({
                "totalWins": len(firstTowerHeraldDataRed),
                "totalGames": totalGamesRedSide,
                "winRate": len(firstTowerHeraldDataRed)/totalGamesRedSide
            })
    else:
        if totalGamesRedSide == 0:
            return Response({
                "totalWins": len(firstTowerHeraldDataBlue),
                "totalGames": totalGamesBlueSide,
                "winRate": len(firstTowerHeraldDataBlue)/totalGamesBlueSide
            })
        else:
            winRate = (len(firstTowerHeraldDataBlue) + len(firstTowerHeraldDataRed))/(totalGamesBlueSide + totalGamesRedSide)
            return Response({
                "totalWins": len(firstTowerHeraldDataBlue) + len(firstTowerHeraldDataRed),
                "totalGames": totalGamesRedSide + totalGamesBlueSide,
                "winRate": winRate
            })
            
@api_view(['PATCH'])
def getHeraldData(request):
    o : TeamStatsRequest = TeamStatsRequest(**json.loads(request.body))
    if len(o.tournamentList) == 0:
        allObjectsBlueSide = GameMetadata.objects.filter(teamBlue=o.teamName, heraldBlueKills__gt=0)
        allObjectsRedSide = GameMetadata.objects.filter(teamRed=o.teamName, heraldRedKills__gt=0)
    else:
        allObjectsBlueSide = GameMetadata.objects.filter(teamBlue=o.teamName, tournament__in=o.tournamentList, heraldBlueKills__gt=0)
        allObjectsRedSide = GameMetadata.objects.filter(teamRed=o.teamName, tournament__in=o.tournamentList, heraldRedKills__gt=0)
        
    winsBlueSide = allObjectsBlueSide.filter(winningTeam=0)
    winsRedSide = allObjectsRedSide.filter(winningTeam=1)
    
    nbWinsBlueSide = len(winsBlueSide)
    nbwinsRedSide = len(winsRedSide)
    
    totalGamesBlueSide = len(allObjectsBlueSide)
    totalGamesRedSide = len(allObjectsRedSide)
    return Response({
        "totalWins": nbWinsBlueSide + nbwinsRedSide,
        "totalGames": totalGamesBlueSide + totalGamesRedSide,
        "winRate": (nbWinsBlueSide + nbwinsRedSide)/(totalGamesBlueSide + totalGamesRedSide)
    })
    
@api_view(['PATCH'])
def getFirstTowerData(request):
    o : TeamStatsRequest = TeamStatsRequest(**json.loads(request.body))
    if len(o.tournamentList) == 0:
        allObjectsBlueSide = GameMetadata.objects.filter(teamBlue=o.teamName, firstTower=0)
        allObjectsRedSide = GameMetadata.objects.filter(teamRed=o.teamName, firstTower=1)
    else:
        allObjectsBlueSide = GameMetadata.objects.filter(teamBlue=o.teamName, tournament__in=o.tournamentList, firstTower=0)
        allObjectsRedSide = GameMetadata.objects.filter(teamRed=o.teamName, tournament__in=o.tournamentList, firstTower=1)
        
    winsBlueSide = allObjectsBlueSide.filter(winningTeam=0)
    winsRedSide = allObjectsRedSide.filter(winningTeam=1)
    
    nbWinsBlueSide = len(winsBlueSide)
    nbwinsRedSide = len(winsRedSide)
    
    totalGamesBlueSide = len(allObjectsBlueSide)
    totalGamesRedSide = len(allObjectsRedSide)
    return Response({
        "totalWins": nbWinsBlueSide + nbwinsRedSide,
        "totalGames": totalGamesBlueSide + totalGamesRedSide,
        "winRate": (nbWinsBlueSide + nbwinsRedSide)/(totalGamesBlueSide + totalGamesRedSide)
    })
    
@api_view(['PATCH'])
def getTeamSide(request):
    o : TeamSideRequest = TeamSideRequest(**json.loads(request.body))
    data = GameMetadata.objects.get(seriesId__exact=o.seriesId, gameNumber__exact=o.gameNumber)
    if data.teamBlue == o.team:
        return Response("Blue")
    elif data.teamRed == o.team:
        return Response("Red")
    
@api_view(['PATCH'])
def getDraftData(request):
    o : TeamDraftDataRequest = TeamDraftDataRequest(**json.loads(request.body))
    
    playedChampionList : list[str] = list()
    seriesIdList : list[int] = list()
    querySeriesId = GameMetadata.objects.filter(Q(teamRed=o.teamName) | Q(teamBlue=o.teamName), tournament__in=o.tournamentList)
    
    
    # Get the list of players
    tempGameMetadata = querySeriesId[0]
    tempSide : int
    if tempGameMetadata.teamBlue == o.teamName:
        tempSide = 0
    elif tempGameMetadata.teamRed == o.teamName:
        tempSide = 1
    
    (data, _, _, _) = getData(querySeriesId[0].seriesId, querySeriesId[0].gameNumber)
    playerList : list [str]= [player.playerName for player in data.gameSnapshotList[0].teams[tempSide].players]

    # Get the list of seriesId where the team played
    for temp in querySeriesId:
        if not(temp.seriesId in seriesIdList):
            seriesIdList.append(temp.seriesId)
    
    # Get the champions picked by the players in the list of seriesId
    championRequest = DraftPlayerPick.objects.filter(seriesId__in=seriesIdList)
    for temp in championRequest:
        if not(temp.championName in playedChampionList) and (temp.sumonnerName in playerList) :
            playedChampionList.append(temp.championName)
    
    # Get the list of patches
    patchList : list = list()
    for temp in querySeriesId:
        patch : str = ".".join([temp.patch.split(".")[0], temp.patch.split(".")[1]])
        if not(patch in patchList):
            patchList.append(patch)
    
    # Gettint the overall draft data
    if o.side in ["Blue", "Red"]:
        queryChampionDraftStats = ChampionDraftStats.objects.filter(tournament__in=o.tournamentList, side__exact=o.side, championName__in=playedChampionList)
        
        res : list[dict] = ChampionDraftStatsSerializer(queryChampionDraftStats.filter(patch__contains=patchList[0]), context={"request": request}, many=True).data
        for patch in patchList[1:]:
            newData : list[dict] = ChampionDraftStatsSerializer(queryChampionDraftStats.filter(patch__contains=patch), context={"request": request}, many=True).data
            res = fuseDataChampionsDraftStats(res, newData)
        
        return Response(res)
    else:
        queryChampionDraftStatsBlue = ChampionDraftStats.objects.filter(tournament__in=o.tournamentList, side__exact="Blue", championName__in=playedChampionList)
        
        resBlue : list[dict] = ChampionDraftStatsSerializer(queryChampionDraftStatsBlue.filter(patch__contains=patchList[0]), context={"request": request}, many=True).data
        for patch in patchList[1:]:
            newData : list[dict] = ChampionDraftStatsSerializer(queryChampionDraftStatsBlue.filter(patch__contains=patch), context={"request": request}, many=True).data
            resBlue = fuseDataChampionsDraftStats(resBlue, newData)
            
        queryChampionDraftStatsRed = ChampionDraftStats.objects.filter(tournament__in=o.tournamentList, side__exact=o.side, championName__in=playedChampionList)
        
        resRed : list[dict] = ChampionDraftStatsSerializer(queryChampionDraftStatsRed.filter(patch__contains=patchList[0]), context={"request": request}, many=True).data
        for patch in patchList[1:]:
            newData : list[dict] = ChampionDraftStatsSerializer(queryChampionDraftStatsRed.filter(patch__contains=patch), context={"request": request}, many=True).data
            resRed = fuseDataChampionsDraftStats(resRed, newData)
        
        res = fuseDataChampionsDraftStats(resBlue, resRed)
        return Response(res)
    
@api_view(['PATCH'])
def getTPPosition(request):
    o : PlayerPositionRequest = PlayerPositionRequest(**json.loads(request.body))
    (data, gameDuration, _, endGameTime) = getData(int(o.seriesId), o.gameNumber)
    participantID = data.gameSnapshotList[0].teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)].participantID
    playerName = data.gameSnapshotList[0].teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)].playerName
    
    team : str = ""
    if data.gameSnapshotList[0].teams[0].isPlayerInTeam(participantID):
        team = "blueTeam"
    elif data.gameSnapshotList[0].teams[1].isPlayerInTeam(participantID):
        team = "redTeam"
        
    tpTriggers = getTPTriggers(data, gameDuration, endGameTime, o.begTime, o.endTime)
    # Building the response
    res : list[list] = [(d["position"]["x"], d["position"]["y"]) for d in tpTriggers[team][playerName]]
    
    return Response(res)

@api_view(['PATCH'])
def getTPPositionGlobal(request):
    o : PlayerPositionGlobalRequest = PlayerPositionGlobalRequest(**json.loads(request.body))
    result : list[dict] = list()
    
    metadataList = GameMetadata.objects.filter(Q(teamRed=o.team) | Q(teamBlue=o.team), tournament__in=o.tournamentList)
    for gameMetadata in tqdm(metadataList):
        data : SeparatedData
        (data, gameDuration, _, endGameTime) = getData(int(gameMetadata.seriesId), gameMetadata.gameNumber)
        participantID = data.gameSnapshotList[0].teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)].participantID
        playerName = data.gameSnapshotList[0].teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)].playerName
        
        team : str = ""
        if data.gameSnapshotList[0].teams[0].isPlayerInTeam(participantID):
            team = "blueTeam"
        elif data.gameSnapshotList[0].teams[1].isPlayerInTeam(participantID):
            team = "redTeam"
            
        tpTriggers = getTPTriggers(data, gameDuration, endGameTime, o.begTime, o.endTime)
        
        result += [(d["position"]["x"], d["position"]["y"]) for d in tpTriggers[team][playerName]]
    
    return Response(result)

@api_view(['PATCH'])
def getMapOpeningsGlobal(request):
    o : PlayerPositionGlobalRequest = PlayerPositionGlobalRequest(**json.loads(request.body))
    result : list[dict] = list()
    metadataList = GameMetadata.objects.filter(Q(teamRed=o.team) | Q(teamBlue=o.team), tournament__in=o.tournamentList)
    for gameMetadata in tqdm(metadataList):
        data : SeparatedData
        (data, gameDuration, _, endGameTime) = getData(int(gameMetadata.seriesId), gameMetadata.gameNumber)
        for event in data.eventList:
            if isinstance(event, ChannelingEndedEvent):
                time = convertTime(event.gameTime, gameDuration, endGameTime)
                if time >= o.begTime and time <= o.endTime and event.channelingType == "recall":
                    participantID = data.gameSnapshotList[0].teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)].participantID
                    position_list = getPlayerPositionHistoryTimeFramed(data, gameMetadata.gameDuration, participantID, time + 1, time + 15)
                    res : list[list] = [pos.toList() for pos in position_list]
                    
                    result += res
                    
    return Response(result)

@api_view(['PATCH'])
def getMapOpenings(request):
    o : PlayerPositionRequest = PlayerPositionRequest(**json.loads(request.body))
    result : list[list] = list()
    (data, gameDuration, _, endGameTime) = getData(int(o.seriesId), o.gameNumber)
    
    participantID = data.gameSnapshotList[0].teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)].participantID
    
    for event in data.eventList:
        if isinstance(event, ChannelingEndedEvent):
            time = convertTime(event.gameTime, gameDuration, endGameTime)
            if time >= o.begTime and time <= o.endTime and event.channelingType == "recall":
                position_list = getPlayerPositionHistoryTimeFramed(data, gameDuration, participantID, time + 1, time + 15)
                res : list[list] = [pos.toList() for pos in position_list]
                
                result += res
                    
    return Response(result)

@api_view(['PATCH'])
def getSideWaveCatch(request):
    o : PlayerPositionRequest = PlayerPositionRequest(**json.loads(request.body))
    
    result : list[list] = list()
    (data, gameDuration, begGameTime, endGameTime) = getData(int(o.seriesId), o.gameNumber)
    topLane : Grid = Grid([Zone(entireTopLaneBoundary)])
    botLane : Grid = Grid([Zone(entireBotLaneBoundary)])
    
    for t in range(o.begTime, o.endTime + 1):
        lowerBound : Snapshot = data.getSnapShotByTime(t, gameDuration)
        upperBound : Snapshot = data.getSnapShotByTime(t + 8, gameDuration)
        
        print(lowerBound.convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime), upperBound.convertGameTimeToSeconds(gameDuration, begGameTime, endGameTime))
        
        playerT = lowerBound.teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)]
        playerT1 = upperBound.teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)]
        
        if (topLane.containsPoint(playerT.position) or botLane.containsPoint(playerT.position)) and playerT1.totalGold - playerT.totalGold > 120:
            result.append(playerT.position.toList())
    
    return Response(result)

@api_view(['PATCH'])
def getSideWaveCatchGlobal(request):
    o : PlayerPositionGlobalRequest = PlayerPositionGlobalRequest(**json.loads(request.body))
    result : list[list] = list()
    metadataList = GameMetadata.objects.filter(Q(teamRed=o.team) | Q(teamBlue=o.team), tournament__in=o.tournamentList)
    for gameMetadata in tqdm(metadataList):
        data : SeparatedData
        (data, gameDuration, _, _) = getData(int(gameMetadata.seriesId), gameMetadata.gameNumber)
        topLane : Grid = Grid([Zone(entireTopLaneBoundary)])
        botLane : Grid = Grid([Zone(entireBotLaneBoundary)])
        
        res : list[list] = list()
        for t in range(o.begTime, o.endTime + 1):
            lowerBound : Snapshot = data.getSnapShotByTime(t, gameDuration)
            upperBound : Snapshot = data.getSnapShotByTime(t + 8, gameDuration)
            
            playerT = lowerBound.teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)]
            playerT1 = upperBound.teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)]
            
            if (topLane.containsPoint(playerT.position) or botLane.containsPoint(playerT.position)) and playerT1.totalGold - playerT.totalGold > 120:
                res.append(playerT.position.toList())
        
        result += res
    return Response(result)