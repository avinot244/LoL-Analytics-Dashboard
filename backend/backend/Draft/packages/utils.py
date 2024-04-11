from dataAnalysis.globals import DATA_PATH

import pandas as pd

def isDraftDownloaded(seriesId : int, gameNumber : int, path):
    df = pd.read_csv(path, sep=";")
    for _, row in df.iterrows():
        if row["SeriesId"] == seriesId and row["GameNumber"] == gameNumber:
            return True
    return False
