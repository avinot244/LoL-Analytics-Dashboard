from dataAnalysis.globals import DATA_PATH
from dataAnalysis.packages.api_calls.GRID.api_calls import *
from dataAnalysis.packages.api_calls.GRID.api_calls import get_team_info_from_seriesId, get_team_members_from_id

from Draft.models import DraftPickOrder

from datetime import datetime
import json
import re


def isDraftDownloaded(seriesId : int, gameNumber : int):
    return DraftPickOrder.objects.filter(seriesId__exact=seriesId, gameNumner__exact=gameNumber).count() > 0

def isTournamentOngoing(tournamentName : str) -> bool:
    # Get today's date
    today_date = datetime.today().date()

    with open(DATA_PATH + "tournament_mapping.json") as json_file: 
        tournament_dict : dict = json.load(json_file)
        tournamentId : int = tournament_dict[tournamentName]
        _, end_date = get_dates_tournament(tournamentId)
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        return today_date < end_date
    

def getPlayerTeam(playerName : str, seriesId : int) -> str:
    teamDict : dict = get_team_info_from_seriesId(seriesId)

    teamIdList : list = list(teamDict.keys())
    teamNameList : list = list(teamDict.values())
    playerListTeam2 : list = get_team_members_from_id(teamIdList[1])

    for player in playerListTeam2:
        x = re.search(player, playerName)
        if x != None:
            return teamNameList[1]
    return teamNameList[0]