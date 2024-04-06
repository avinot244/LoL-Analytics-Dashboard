import pandas as pd
from behaviorADC.models import BehaviorJungle

csv_file_path = "./databases/behavior/behavior/behavior_Jungle.csv"
df = pd.read_csv(csv_file_path, sep=";")


for index, row in df.iterrows():
    behaviorJungle = BehaviorJungle(
        date = row["Date"],
        tournament = row["Tournament"],
        matchId = row["MatchId"],
        summonnerName = row["SummonnerName"],
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
        riverTopPresence = row["riverTopPresence"]
    )


    behaviorJungle.save()

print("CSV data has been loaded into the Django database.")