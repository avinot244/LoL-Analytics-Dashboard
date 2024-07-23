import pandas as pd
from Draft.models import ChampionBanStats
from tqdm import tqdm

def refresh_championBanStats():
    csv_champion_bans_stats : str = "./databases/drafts/champion_bans_stats.csv"
    df_champion_bans_stats : pd.DataFrame = pd.read_csv(csv_champion_bans_stats, sep=";", dtype={
        "ChampionName": 'string',
        "Patch": 'string',
        "Tournament": 'string',
        "Side": 'string',
        "GlobalBanRate": 'float64',
        "BanRate1Rota": 'float64',
        "BanRate2Rota": 'float64'
    })

    for index, row in tqdm(df_champion_bans_stats.iterrows(), total=df_champion_bans_stats.shape[0]):
        championBanStats = ChampionBanStats(
            championName = row["ChampionName"],
            patch = row["Patch"],
            tournament = row["Tournament"],
            side = row["Side"],
            globalBanRate = row["GlobalBanRate"],
            banRate1Rota = row["BanRate1Rota"],
            banRate2Rota = row["BanRate2Rota"],
        )
        if not(ChampionBanStats.objects.filter(
            championName = row["ChampionName"],
            patch = row["Patch"],
            tournament = row["Tournament"],
            side = row["Side"],
            globalBanRate = row["GlobalBanRate"],
            banRate1Rota = row["BanRate1Rota"],
            banRate2Rota = row["BanRate2Rota"],
        ).count() > 0):
            championBanStats.save()