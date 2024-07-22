import pandas as pd
from ..models import ChampionDraftStats
from tqdm import tqdm

csv_champion_draft_stats : str = "./databases/drafts/champion_draft_stats.csv"
df_champion_draft_stats : pd.DataFrame = pd.read_csv(csv_champion_draft_stats, sep=";", dtype={
    "ChampionName": 'string',
    "Patch": 'string',
    "Tournament": 'string',
    "Side": 'string',
    "WinRate": 'float64',
    "GlobalPickRate": 'float64',
    "PickRate1Rota": 'float64',
    "PickRate2Rota": 'float64',
    "GlobalBanRate": 'float64',
    "BanRate1Rota": 'float64',
    "BanRate2Rota": 'float64',
    "DraftPresence": 'float64',
    "MostPopularPickOrder": 'int64',
    "BlindPick": 'float64',
    "MostPopularRole": 'string'
})

for index, row in tqdm(df_champion_draft_stats.iterrows(), total=df_champion_draft_stats.shape[0]):
    championDraftStats = ChampionDraftStats(
        championName = row["ChampionName"],
        patch = row["Patch"],
        tournament = row["Tournament"],
        side = row["Side"],
        winRate = row["WinRate"],
        globalPickRate = row["GlobalPickRate"],
        pickRate1Rota = row["PickRate1Rota"],
        pickRate2Rota = row["PickRate2Rota"],
        globalBanRate = row["GlobalBanRate"],
        banRate1Rota = row["BanRate1Rota"],
        banRate2Rota = row["BanRate2Rota"],
        draftPresence = row["DraftPresence"],
        mostPopularPickOrder = row["MostPopularPickOrder"],
        blindPick = row["BlindPick"],
        mostPopularRole = row["MostPopularRole"]
    )
    
    if not(ChampionDraftStats.objects.filter(
        championName = row["ChampionName"],
        patch = row["Patch"],
        tournament = row["Tournament"],
        side = row["Side"],
        winRate = row["WinRate"],
        globalPickRate = row["GlobalPickRate"],
        pickRate1Rota = row["PickRate1Rota"],
        pickRate2Rota = row["PickRate2Rota"],
        globalBanRate = row["GlobalBanRate"],
        banRate1Rota = row["BanRate1Rota"],
        banRate2Rota = row["BanRate2Rota"],
        draftPresence = row["DraftPresence"],
        mostPopularPickOrder = row["MostPopularPickOrder"],
        blindPick = row["BlindPick"],
        mostPopularRole = row["MostPopularRole"]
    ).count() > 0):
        championDraftStats.save()
print("Draft stats imported")