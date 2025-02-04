import json
from tqdm import tqdm

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

from .packages.Parsers.Separated.Game.SeparatedData import SeparatedData
from .models import GameMetadata
from .serializer import GameMetadataSerializer
from .globals import SIDES, ROLE_LIST, DATE_LIMIT
from .packages.utils_stuff.utils_func import getData
from .request_models import PlayerPositionRequest, WardPlacedRequest, GameTimeFrameRequest, TeamStatsRequest, GetGameRequest, TeamSideRequest, PlayerPositionGlobalRequest, TeamDraftDataRequest
from .packages.Parsers.Separated.Game.getters import getResetTriggers, getWardTriggers, getPlayerPositionHistoryTimeFramed, getKillTriggers


from Draft.utils import fuseQueriesChampionDraftStats
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
def getPlayerResetPositionsGlobal(request):
    o : PlayerPositionGlobalRequest = PlayerPositionGlobalRequest(**json.loads(request.body))
    result : list[dict] = list()
    
    metadataList = GameMetadata.objects.filter(Q(teamRed=o.team) | Q(teamBlue=o.team), tournament__in=o.tournamentList)
    for gameMetadata in tqdm(metadataList):
        data : SeparatedData
        (data,_ , _, _) = getData(int(gameMetadata.seriesId), gameMetadata.gameNumber)
        participantID = data.gameSnapshotList[0].teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)].participantID
        playerName = data.gameSnapshotList[0].teams[SIDES.index(o.side)].players[ROLE_LIST.index(o.role)].playerName
        
        team : str = ""
        if data.gameSnapshotList[0].teams[0].isPlayerInTeam(participantID):
            team = "blueTeam"
        elif data.gameSnapshotList[0].teams[1].isPlayerInTeam(participantID):
            team = "redTeam"
        
        resetTriggers = getResetTriggers(data, gameMetadata.gameDuration, o.begTime, o.endTime, verbose=False)[team][playerName]
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
    
    wardTriggers = getWardTriggers(data, gameDuration, endGameTime, o.begTime, o.endTime)[team][playerName]
    
    # Building the response
    res : list[list] = [(d["position"]["x"], d["position"]["z"]) for d in wardTriggers]
    
    return Response(res)

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
    querySeriesId = GameMetadata.objects.filter(Q(teamRed=o.teamName) | Q(teamBlue=o.teamName), tournament__in=o.tournamentList, patch__contains=o.patch)
    
    
    # Get the list of players
    tempGameMetadata = querySeriesId[0]
    tempSide : int
    if tempGameMetadata.teamBlue == o.teamName:
        tempSide = 0,
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
    
    # Getting the overall data of the champions picked by the players from the team o.teamName during the tournaments in o.tournamentList
    if o.side in ["Blue", "Red"]:
        queryChampionDraftStats = ChampionDraftStats.objects.filter(tournament__in=o.tournamentList, side__exact=o.side, championName__in=playedChampionList, patch__contains=o.patch)
        serializer = ChampionDraftStatsSerializer(queryChampionDraftStats, context={"request": request}, many=True)
        print(json.dumps(serializer.data, indent=4))
        return Response(serializer.data)
    else: 
        queryBlue = ChampionDraftStats.objects.filter(tournament__in=o.tournamentList, side__exact="Blue", championName__in=playedChampionList, patch__contains=o.patch)
        queryRed = ChampionDraftStats.objects.filter(tournament__in=o.tournamentList, side__exact="Red", championName__in=playedChampionList, patch__contains=o.patch)
        
        return Response(fuseQueriesChampionDraftStats(queryRed, queryBlue))