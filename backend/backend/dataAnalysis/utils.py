from .globals import DATA_PATH

import pandas as pd

def isGameDownloaded(seriesId : int, gameNumber : int):
    df = pd.read_csv(DATA_PATH + "games/data_metadata.csv", sep=";")
    for _, row in df.iterrows():
        if row["SeriesId"] == seriesId and row["gameNumber"] == gameNumber:
            return True
    return False

    