import pandas as pd
from behaviorADC.models import BehaviorMid
from tqdm import tqdm

csv_file_path = "./databases/behavior/behavior/behavior_Mid.csv"
df = pd.read_csv(csv_file_path, sep=";")


for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    behaviorMid = BehaviorMid(
        date = row["Date"],
        tournament = row["Tournament"],
        matchId = row["MatchId"],
        seriesId = row["SeriesId"],
        patch = row["Patch"],
        summonnerName = row["SummonnerName"],
        xpd15 = row["XPD@15"],
        gd15 = row["GD@15"],
        csMin = row["CS/Min"],
        kills = row["Kills"],
        deaths = row["Deaths"],
        assists = row["Assists"],
        kp = row["KP%"],
        wardPlaced = row["WardPlaced"],
        wardKilled = row["WardKilled"],
        dpm = row["Damage/Min"],
        totalDamageDealtToBuilding = row["TotalDamageDealtToBuilding"],
        totalDamageDealtToObjectives = row["TotalDamageDealtToObjectives"],
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
        gameNumber = row["GameNumber"],
    )


    behaviorMid.save()

print("CSV data has been loaded into the Django database.")