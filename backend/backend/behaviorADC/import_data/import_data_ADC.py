import pandas as pd
from behaviorADC.models import BehaviorADC
from tqdm import tqdm

csv_file_path = "./databases/behavior/behavior/behavior_ADC.csv"
df = pd.read_csv(csv_file_path, sep=";")


for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    behaviorADC = BehaviorADC(
        date = row["Date"],
        tournament = row["Tournament"],
        matchId = row["MatchId"],
        summonnerName = row["SummonnerName"],
        patch = row["Patch"],
        seriesId = row["SeriesId"],
        xpd15 = row["XPD@15"],
        gd15 = row["GD@15"],
        csMin = row["CS/Min"],
        kills = row["Kills"],
        deaths = row["Deaths"],
        assists = row["Assists"],
        kp = row["KP%"],
        dpm = row["Damage/Min"],
        jungleProximity = row["JungleProximity"],
        botLanePresence = row["botLanePresence"],
        riverBotPresence = row["riverBotPresence"],
        gameNumber = row["GameNumber"]
    )


    behaviorADC.save()

print("CSV data has been loaded into the Django database.")