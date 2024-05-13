import pandas as pd
from tqdm import tqdm
from ..models import ChampionPool

csv_player_championPool : str = "./databases/drafts/player_championPool.csv"
df_player_championPool : pd.DataFrame = pd.read_csv(csv_player_championPool, sep=";")

for index, row in tqdm(df_player_championPool.iterrows(), total=df_player_championPool.shape[0]):
    championPool = ChampionPool(
        summonnerName=row["SummonnerName"],
        championName=row["ChampionName"],
        tournament=row["Tournament"],
        globalPickRate=row["GlobalPickRate"],
        winRate=row["WinRate"],
        nbGames=row["NbGames"],
        kda=row["KDA"],
    )

    if not(ChampionPool.objects.filter(
        summonnerName=row["SummonnerName"],
        championName=row["ChampionName"],
        tournament=row["Tournament"],
        globalPickRate=row["GlobalPickRate"],
        winRate=row["WinRate"],
        nbGames=row["NbGames"],
        kda=row["KDA"],
    ).count() > 0):
        championPool.save()

print("Saved champion pools")