import pandas as pd
from Draft.models import DraftPlayerPick
from tqdm import tqdm

def refresh_draftPlayerPick():
    csv_draft_player_pick : str = "./databases/drafts/draft_player_picks.csv"
    df_draft_player_pick : pd.DataFrame = pd.read_csv(csv_draft_player_pick, sep=";")
    for _, row in tqdm(df_draft_player_pick.iterrows(), total=df_draft_player_pick.shape[0]):
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

        if not(DraftPlayerPick.objects.filter(
            date=row["Date"], 
            tournament=row["Tournament"], 
            patch=row["Patch"], 
            seriesId=row["SeriesId"], 
            championName=row["ChampionName"], 
            role=row["Role"], 
            gameNumber=row["GameNumber"]).count() > 0):
            
            draftPlayerPick.save()