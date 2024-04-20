from dataAnalysis.globals import DATA_PATH
from dataAnalysis.packages.api_calls.GRID.api_calls import *

import pandas as pd
from datetime import datetime
import json


def isDraftDownloaded(seriesId : int, gameNumber : int, path):
    df = pd.read_csv(path, sep=";")
    for _, row in df.iterrows():
        if row["SeriesId"] == seriesId and row["GameNumber"] == gameNumber:
            return True
    return False

def isTournamentOngoing(tournamentName : str) -> bool:
    # Get today's date
    today_date = datetime.today().date()

    with open(DATA_PATH + "tournament_mapping.json") as json_file: 
        tournament_dict : dict = json.load(json_file)
        tournamentId : int = tournament_dict[tournamentName]
        _, end_date = get_dates_tournament(tournamentId)
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        return today_date < end_date