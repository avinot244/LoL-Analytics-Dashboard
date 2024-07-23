from dataAnalysis.globals import DATA_PATH, ROLE_LIST
from django.db.models.query import QuerySet

from .models import *

import pandas as pd
from tqdm import tqdm

def import_draftPickOrder():
    csv_draft_pick_order : str = "./databases/drafts/draft_pick_order.csv"

    df_draft_pick_order : pd.DataFrame = pd.read_csv(csv_draft_pick_order, sep=";", dtype={
        "Date": 'string',
        "Tournament": 'string',
        "Patch": 'string',
        "SeriesId": 'int64',
        "Winner": 'int64',
        "GameNumber": 'int64',
        "teamBlue": 'string',
        "teamRed": 'string',
        "BB1": 'string',
        "BB2": 'string',
        "BB3": 'string',
        "BB4": 'string',
        "BB5": 'string',
        "BP1": 'string',
        "BP2": 'string',
        "BP3": 'string',
        "BP4": 'string',
        "BP5": 'string',
        "RB1": 'string',
        "RB2": 'string',
        "RB3": 'string',
        "RB4": 'string',
        "RB5": 'string',
        "RP1": 'string',
        "RP2": 'string',
        "RP3": 'string',
        "RP4": 'string',
        "RP5": 'string',
    })
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

def delete_draftStats():
    queryChampionDraftStats = ChampionDraftStats.objects.all()
    for res in tqdm(queryChampionDraftStats):
        res.delete()

   

def import_banStats():
    csv_champion_ban_stats : str = "./databases/drafts/champion_bans_stats.csv"
    df_champion_ban_stats : pd.DataFrame = pd.read_csv(csv_champion_ban_stats, sep=";", dtype={
        "ChampionName": 'string',
        "Patch": 'string',
        "Tournament": 'string',
        "Side": 'string',
        "GlobalBanRate": 'float64',
        "BanRate1Rota": 'float64',
        "BanRate2Rota": 'float64'
    })
    
    for _, row in tqdm(df_champion_ban_stats.iterrows(), total=df_champion_ban_stats.shape[0]):
        championBanStats = ChampionBanStats(
            championName = row["ChampionName"],
            patch = row["Patch"],
            tournament = row["Tournament"],
            side = row["Side"],
            globalBanRate = row["GlobalBanRate"],
            banRate1Rota = row["BanRate1Rota"],
            banRate2Rota = row["BanRate2Rota"]
        )
        if not(ChampionBanStats.objects.filter(
            championName = row["ChampionName"],
            patch = row["Patch"],
            tournament = row["Tournament"],
            side = row["Side"],
            globalBanRate = row["GlobalBanRate"],
            banRate1Rota = row["BanRate1Rota"],
            banRate2Rota = row["BanRate2Rota"]
        ).count() > 0):
            championBanStats.save()
    # ChampionBanStats

def import_draftStats():
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

def computeFusedMapping(championNameList1 : list, championNameList2 : list) -> dict:
    res : dict = dict()
    for championName in championNameList1:
        if championName in championNameList2: # if both champion are in the list
            res[championName] = 0
        else: # if only championName is in list 1
            res[championName] = 1
    
    for championName in championNameList2:
        if not(championName in championNameList1): # we get the champs from list 2 that are not common to list 1
            res[championName] = 2
    
    return res

def fuseQueriesChampionDraftStats(query1 : QuerySet, query2 : QuerySet):
    object1 : ChampionDraftStats
    object2 : ChampionDraftStats
    
    championNameList1 : list = [o.championName for o in query1]
    championNameList2 : list = [o.championName for o in query2]
    
    mapping : dict = computeFusedMapping(championNameList1, championNameList2)
    
    res : list = list()
    
    for champion_name, distsribution in mapping.values():
        if distsribution == 0:
            object1 = query1.get(championName__exact=champion_name)
            object2 = query2.get(championName__exact=champion_name)
            fusedObject = ChampionDraftStats(
                championName = object1.championName,
                patch = object1.patch,
                tournament = object1.tournament,
                side = "Both",
                winRate = (object1.winRate + object2.winRate) / 2,
                globalPickRate = (object1.globalPickRate + object2.globalPickRate) / 2,
                pickRate1Rota = (object1.pickRate1Rota + object2.pickRate1Rota) / 2,
                pickRate2Rota = (object1.pickRate2Rota + object2.pickRate2Rota) / 2,
                globalBanRate = (object1.globalBanRate + object2.globalBanRate) / 2,
                banRate1Rota = (object1.banRate1Rota + object2.banRate1Rota) / 2,
                banRate2Rota = (object1.banRate2Rota + object2.banRate2Rota) / 2,
                draftPresence = (object1.draftPresence + object2.draftPresence) / 2,
                mostPopularPickOrder = (object1.mostPopularPickOrder + object2.mostPopularPickOrder) / 2,
                blindPick = (object1.blindPick + object2.blindPick) / 2,
                mostPopularRole = object1.mostPopularRole
            )
            
            res.append({
                "pk": fusedObject.pk,
                "championName": fusedObject.championName,
                "patch": fusedObject.patch,
                "tournament": fusedObject.tournament,
                "side": fusedObject.side,
                "mostPopularRole": fusedObject.mostPopularRole,
                "winRate": fusedObject.winRate,
                "globalPickRate": fusedObject.globalPickRate,
                "pickRate1Rota": fusedObject.pickRate1Rota,
                "pickRate2Rota": fusedObject.pickRate2Rota,
                "globalBanRate": fusedObject.globalBanRate,
                "banRate1Rota": fusedObject.banRate1Rota,
                "banRate2Rota": fusedObject.banRate2Rota,
                "draftPresence": fusedObject.draftPresence,
                "mostPopularPickOrder": fusedObject.mostPopularPickOrder,
                "blindPick": fusedObject.blindPick
            })
        elif distsribution == 1:
            object1 = query1.get(championName__exact=champion_name)
            res.append({
                "pk": object1.pk,
                "championName": object1.championName,
                "patch": object1.patch,
                "tournament": object1.tournament,
                "side": object1.side,
                "mostPopularRole": object1.mostPopularRole,
                "winRate": object1.winRate,
                "globalPickRate": object1.globalPickRate,
                "pickRate1Rota": object1.pickRate1Rota,
                "pickRate2Rota": object1.pickRate2Rota,
                "globalBanRate": object1.globalBanRate,
                "banRate1Rota": object1.banRate1Rota,
                "banRate2Rota": object1.banRate2Rota,
                "draftPresence": object1.draftPresence,
                "mostPopularPickOrder": object1.mostPopularPickOrder,
                "blindPick": object1.blindPick
            })
        elif distsribution == 2:
            object2 = query2.get(championName__exact=champion_name)
            res.append({
                "pk": object2.pk,
                "championName": object2.championName,
                "patch": object2.patch,
                "tournament": object2.tournament,
                "side": object2.side,
                "mostPopularRole": object2.mostPopularRole,
                "winRate": object2.winRate,
                "globalPickRate": object2.globalPickRate,
                "pickRate1Rota": object2.pickRate1Rota,
                "pickRate2Rota": object2.pickRate2Rota,
                "globalBanRate": object2.globalBanRate,
                "banRate1Rota": object2.banRate1Rota,
                "banRate2Rota": object2.banRate2Rota,
                "draftPresence": object2.draftPresence,
                "mostPopularPickOrder": object2.mostPopularPickOrder,
                "blindPick": object2.blindPick
            })
                
    return res

def fuseQueriesChampionBansStats(query1 : QuerySet, query2 : QuerySet):
    object1 : ChampionBanStats
    object2 : ChampionBanStats
    
    championNameList1 : list = [o.championName for o in query1]
    championNameList2 : list = [o.championName for o in query2]
    
    mapping : dict = computeFusedMapping(championNameList1, championNameList2)
    
    res : list = list()
    for champion_name, distsribution in mapping.values():
        if distsribution == 0:
            object1 = query1.get(championName__exact=champion_name)
            object2 = query2.get(championName__exact=champion_name)
            fusedObject = ChampionBanStats(
                championName = object1.championName,
                patch = object1.patch,
                tournament = object1.tournament,
                side = "Both",
                globalBanRate = (object1.globalBanRate + object2.globalBanRate) / 2,
                banRate1Rota = (object1.banRate1Rota + object2.banRate1Rota) / 2,
                banRate2Rota = (object1.banRate2Rota + object2.banRate2Rota) / 2
            )
            
            res.append({
                "pk": fusedObject.pk,
                "championName": fusedObject.championName,
                "patch": fusedObject.patch,
                "tournament": fusedObject.tournament,
                "side": fusedObject.side,
                "globalBanRate": fusedObject.globalBanRate,
                "banRate1Rota": fusedObject.banRate1Rota,
                "banRate2Rota": fusedObject.banRate2Rota
            })
        elif distsribution == 1:
            object1 = query1.get(championName__exact=champion_name)
            res.append({
                "pk": object1.pk,
                "championName": object1.championName,
                "patch": object1.patch,
                "tournament": object1.tournament,
                "side": object1.side,
                "globalBanRate": object1.globalBanRate,
                "banRate1Rota": object1.banRate1Rota,
                "banRate2Rota": object1.banRate2Rota
            })
        elif distsribution == 2:
            object2 = query2.get(championName__exact=champion_name)
            res.append({
                "pk": object2.pk,
                "championName": object2.championName,
                "patch": object2.patch,
                "tournament": object2.tournament,
                "side": object2.side,
                "globalBanRate": object2.globalBanRate,
                "banRate1Rota": object2.banRate1Rota,
                "banRate2Rota": object2.banRate2Rota
            })
    return res