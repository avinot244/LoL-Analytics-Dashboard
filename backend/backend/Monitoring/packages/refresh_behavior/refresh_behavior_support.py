import pandas as pd
from behaviorADC.models import BehaviorSupport
from tqdm import tqdm

def refresh_behavior_support():
    csv_file_path = "./databases/behavior/behavior/behavior_Support.csv"
    df = pd.read_csv(csv_file_path, sep=";")


    for _, row in tqdm(df.iterrows(), total=df.shape[0]):
        behaviorSupport = BehaviorSupport(
            date = row["Date"],
            tournament = row["Tournament"],
            matchId = row["MatchId"],
            seriesId = row["SeriesId"],
            patch = row["Patch"],
            summonnerName = row["SummonnerName"],
            xpd15 = row["XPD@15"],
            gd15 = row["GD@15"],
            deaths = row["Deaths"],
            kp = row["KP%"],
            wardPlaced = row["WardPlaced"],
            wardKilled = row["WardKilled"],
            dpm = row["Damage/Min"],
            jungleProximity = row["JungleProximity"],
            topLanePresence = row["topLanePresence"],
            midLanePresence = row["midLanePresence"],
            botLanePresence = row["botLanePresence"],
            jungleAllyTopPresence = row["jungleAllyTopPresence"],
            jungleAllyBotPresence = row["jungleAllyBotPresence"],
            jungleEnemyTopPresence = row["jungleEnemyTopPresence"],
            jungleEnemyBotPresence = row["jungleEnemyBotPresence"],
            riverBotPresence = row["riverBotPresence"],
            riverTopPresence = row["riverTopPresence"],
            gameNumber = row["GameNumber"]
        )

        behaviorSupport.save()
