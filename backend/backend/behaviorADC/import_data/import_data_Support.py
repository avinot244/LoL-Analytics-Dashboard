import pandas as pd
from behaviorADC.models import BehaviorSupport

csv_file_path = "./databases/behavior/behavior/behavior_Support.csv"
df = pd.read_csv(csv_file_path, sep=";")


for index, row in df.iterrows():
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

print("CSV data has been loaded into the Django database.")