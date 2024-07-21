import pandas as pd
from behaviorADC.models import BehaviorJungle
from tqdm import tqdm


def refresh_behavior_jungle():
    csv_file_path = "./databases/behavior/behavior/behavior_Jungle.csv"
    df = pd.read_csv(csv_file_path, sep=";")


    for _, row in tqdm(df.iterrows(), total=df.shape[0]):
        behaviorJungle = BehaviorJungle(
            date = row["Date"],
            tournament = row["Tournament"],
            matchId = row["MatchId"],
            summonnerName = row["SummonnerName"],
            patch = row["Patch"],
            seriesId = row["SeriesId"],
            xpd15 = row["XPD@15"],
            gd15 = row["GD@15"],
            kills = row["Kills"],
            deaths = row["Deaths"],
            assists = row["Assists"],
            kp = row["KP%"],
            dpm = row["Damage/Min"],
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


        behaviorJungle.save()
