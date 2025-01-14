import json
from rest_framework.decorators import api_view
from rest_framework.response import Response

from dataAnalysis.globals import SIDES, ROLE_LIST
from dataAnalysis.packages.utils_stuff.utils_func import getData
from .request_models import PlayerPositionRequest, WardPlacedRequest, KillEventsRequest, GrubsDrakeStatsRequest
from dataAnalysis.packages.Parsers.Separated.Game.getters import getResetTriggers, getWardTriggers, getPlayerPositionHistoryTimeFramed, getKillTriggers

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
    
    # allObjects = 