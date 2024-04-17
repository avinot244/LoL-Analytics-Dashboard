import pandas as pd
from behaviorADC.models import BehaviorTop

csv_file_path = "./databases/behavior/behavior/behavior_Top.csv"
df = pd.read_csv(csv_file_path, sep=";")


for index, row in df.iterrows():
    behaviorTop = BehaviorTop(
        date = row["Date"],
        tournament = row["Tournament"],
        matchId = row["MatchId"],
        summonnerName = row["SummonnerName"],
        seriesId = row["SeriesId"],
        xpd15 = row["XPD@15"],
        gd15 = row["GD@15"],
        csMin = row["CS/Min"],
        kills = row["Kills"],
        deaths = row["Deaths"],
        assists = row["Assists"],
        kp = row["KP%"],
        wardPlaced = row["WardPlaced"],
        dpm = row["Damage/Min"],
        totalDamageDealtToBuilding = row["TotalDamageDealtToBuilding"],
        totalDamageDealtToObjectives = row["TotalDamageDealtToObjectives"],
        jungleProximity = row["JungleProximity"],
        topLanePresence = row["topLanePresence"],
        jungleAllyTopPresence = row["jungleAllyTopPresence"],
        jungleEnemyTopPresence = row["jungleEnemyTopPresence"],
        riverTopPresence = row["riverTopPresence"],
        gameNumber = row["GameNumber"]
    )


    behaviorTop.save()

print("CSV data has been loaded into the Django database.")