import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

from .models import GameMetadata
from .serializer import GameMetadataSerializer
from .globals import SIDES, ROLE_LIST
from .packages.utils_stuff.utils_func import getData
from .request_models import PlayerPositionRequest, WardPlacedRequest, KillEventsRequest, GrubsDrakeStatsRequest
from .packages.Parsers.Separated.Game.getters import getResetTriggers, getWardTriggers, getPlayerPositionHistoryTimeFramed, getKillTriggers

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
def getPlayerResetPositions(request):
    o : PlayerPositionRequest = PlayerPositionRequest(**json.loads(request.body))
    (data, gameDuration, _, _) = getData(int(o.seriesId), o.gameNumber)
    
    participantID = data.gameSnapshotList[0].teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)].participantID
    playerName = data.gameSnapshotList[0].teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)].playerName
    
    team : str = ""
    if data.gameSnapshotList[0].teams[0].isPlayerInTeam(participantID):
        team = "blueTeam"
    elif data.gameSnapshotList[0].teams[1].isPlayerInTeam(participantID):
        team = "redTeam"
    
    resetTriggers = getResetTriggers(data, gameDuration, o.begTime, o.endTime)[team][playerName]
    
    # Building the response
    res : list[list] = [(d["position"]["x"], d["position"]["y"]) for d in resetTriggers]
    
    return Response(res)

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
    
    wardTriggers = getWardTriggers(data, gameDuration, endGameTime, o.begTime, o.endTime)[team][playerName]
    
    # Building the response
    res : list[list] = [(d["position"]["x"], d["position"]["z"]) for d in wardTriggers]
    
    return Response(res)

@api_view(['PATCH'])
def getKillEvents(request):
    o : KillEventsRequest = KillEventsRequest(**json.loads(request.body))
    (data, gameDuration, _, endGameTime) = getData(int(o.seriesId), o.gameNumber)

    killEvents = getKillTriggers(data, gameDuration, endGameTime, o.begTime, o.endTime)[o.team]
    
    return Response(killEvents)

@api_view(['GET'])
def getGrubsDrakeStats(request):
    o : GrubsDrakeStatsRequest = GrubsDrakeStatsRequest(**json.loads(request.body))
    
    if len(o.tournamentList) == 0:
        allObjectsBlueSide = GameMetadata.objects.filter(teamBlue=o.teamName)
        allObjectsRedSide = GameMetadata.objects.filter(teamRed=o.teamName)
    else:
        allObjectsBlueSide = GameMetadata.objects.filter(teamBlue=o.teamName, tournament__in=o.tournamentList)
        allObjectsRedSide = GameMetadata.objects.filter(teamRed=o.teamName, tournament__in=o.tournamentList)
    
    response : list[dict] = list()
    
    for nGrubs in range(0, 7):
        for nDrake in range(0, 5):
            # For blue side
            blueData = allObjectsBlueSide.filter(voidGrubsBlueKills=nGrubs, dragonBlueKills=nDrake)
            nbGamesBlue : int = len(blueData)
            nbWinBlue = len(blueData.filter(winningTeam=0))
            
            # For red side
            redData = allObjectsRedSide.filter(voidGrubsRedKills=nGrubs, dragonRedKills=nDrake)
            nbGamesRed : int = len(redData)
            nbWinRed = len(redData.filter(winningTeam=1))
            
            if nbGamesRed + nbGamesRed == 0:
                response.append({
                    "nGrubs": nGrubs,
                    "nDrake": nDrake,
                    "winRate": -1,
                    "nbGames": nbGamesBlue + nbGamesRed
                })
            else:
                response.append({
                    "nGrubs": nGrubs,
                    "nDrake": nDrake,
                    "winrate": (nbWinBlue + nbWinRed)/(nbGamesBlue+ nbGamesRed),
                    "nbGames": nbGamesBlue + nbGamesRed
                })
    
    # We want a list of triples [nGrubs, nDrakes, winRate, nbGames]
    
    return Response(response)