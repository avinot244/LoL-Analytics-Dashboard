from .globals import DATA_PATH

import pandas as pd

def isGameDownloaded(seriesId : int):
    df = pd.read_csv(DATA_PATH + "games/data_metadata.csv", sep=";")
    return (seriesId in df["SeriesId"].unique().tolist())

    