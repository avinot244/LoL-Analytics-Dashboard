from dataAnalysis.globals import DATA_PATH, ROLE_LIST

from .models import *

import pandas as pd

def import_draftPickOrder():
    csv_draft_pick_order : str = "./databases/drafts/draft_pick_order.csv"

    df_draft_pick_order : pd.DataFrame = pd.read_csv(csv_draft_pick_order, sep=";")
    for index, row in df_draft_pick_order.iterrows():
        draftPickOrder = DraftPickOrder(
            date = row["Date"],
            tournament = row["Tournament"],
            patch = row["Patch"],
            seriesId = row["SeriesId"],
            winner = row["Winner"],
            gameNumner = row["GameNumber"],
            teamBlue = row["teamBlue"],
            teamRed = row["teamRed"],
            bb1 = row["BB1"],
            bb2 = row["BB2"],
            bb3 = row["BB3"],
            bb4 = row["BB4"],
            bb5 = row["BB5"],
            bp1 = row["BP1"],
            bp2 = row["BP2"],
            bp3 = row["BP3"],
            bp4 = row["BP4"],
            bp5 = row["BP5"],
            rb1 = row["RB1"],
            rb2 = row["RB2"],
            rb3 = row["RB3"],
            rb4 = row["RB4"],
            rb5 = row["RB5"],
            rp1 = row["RP1"],
            rp2 = row["RP2"],
            rp3 = row["RP3"],
            rp4 = row["RP4"],
            rp5 = row["RP5"]
        )
        if not(DraftPickOrder.objects.filter(
            date = row["Date"],
            tournament = row["Tournament"],
            patch = row["Patch"],
            seriesId = row["SeriesId"],
            winner = row["Winner"],
            gameNumner = row["GameNumber"],
            teamBlue = row["teamBlue"],
            teamRed = row["teamRed"],
            bb1 = row["BB1"],
            bb2 = row["BB2"],
            bb3 = row["BB3"],
            bb4 = row["BB4"],
            bb5 = row["BB5"],
            bp1 = row["BP1"],
            bp2 = row["BP2"],
            bp3 = row["BP3"],
            bp4 = row["BP4"],
            bp5 = row["BP5"],
            rb1 = row["RB1"],
            rb2 = row["RB2"],
            rb3 = row["RB3"],
            rb4 = row["RB4"],
            rb5 = row["RB5"],
            rp1 = row["RP1"],
            rp2 = row["RP2"],
            rp3 = row["RP3"],
            rp4 = row["RP4"],
            rp5 = row["RP5"]).count() > 0):
            
            draftPickOrder.save()
    print("Draft Pick Order imported")

def import_draftPlayerPick():
    csv_draft_player_pick : str = "./databases/drafts/draft_player_picks.csv"
    df_draft_player_pick : pd.DataFrame = pd.read_csv(csv_draft_player_pick, sep=";")
    for index, row in df_draft_player_pick.iterrows():
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
    print("Draft Player Pick imported")

def import_draft():
    import_draftPickOrder()
    import_draftPlayerPick()

def import_draftStats():
    csv_champion_draft_stats : str = "./databases/drafts/champion_draft_stats.csv"
    df_champion_draft_stats : pd.DataFrame = pd.read_csv(csv_champion_draft_stats, sep=";")

    for index, row in df_champion_draft_stats.iterrows():
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
            mostPopularPickOrder = row["MostPopularPickOrder"],
            blindPick = row["BlindPick"],
            mostPopularRole = row["MostPopularRole"]
        ).count() > 0):
            championDraftStats.save()
    print("Draft stats imported")

def import_championPools():
    csv_player_championPool : str = "./databases/drafts/player_championPool.csv"
    df_player_championPool : pd.DataFrame = pd.read_csv(csv_player_championPool, sep=";")

    for index, row in df_player_championPool.iterrows():
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
    print("Champion pools imported")