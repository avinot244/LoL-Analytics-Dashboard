import pandas as pd
from .models import DraftPlayerPick

csv_player_picks : str = "./databases/drafts/draft_player_picks.csv"

df_player_picks = pd.read_csv(csv_player_picks, sep=";")
for index, row in df_player_picks.iterrows():
    draftPlayerPick = DraftPlayerPick(
        date = row["Date"],
        tournament = row["Tournament"],
        patch = row["Patch"],
        seriesId = row["SeriesId"],
        sumonnerName = row["SummonnerName"],
        championName = row["ChampionName"],
        role = row["Role"],
        gameNumber = row["GameNumber"],
    )
    draftPlayerPick.save()

print("Saved players picks")
