from dataAnalysis.globals import DATA_PATH
from dataAnalysis.packages.api_calls.GRID.api_calls import *

from Draft.models import DraftPickOrder

import pandas as pd
from datetime import datetime
import json


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