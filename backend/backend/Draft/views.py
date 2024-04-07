from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import DraftPickOrder, DraftPlayerPick
from dataAnalysis.packages.api_calls.GRID.api_calls import get_tournament_from_seriesId
from dataAnalysis.packages.utils_stuff.utils_func import getData
from dataAnalysis.globals import DATA_PATH

import pandas as pd
import requests
import os

@api_view(['POST'])
def saveDrafts(request):
    data_metadata : pd.DataFrame = pd.read_csv(DATA_PATH + "games/data_metadata.csv", sep=";")

    for idx, row in data_metadata.iterrows():
        file_name : str = row["Name"]
        gameNumber : int = int(file_name.split("_")[2][0])
        seriesId : int = row["SeriesId"]
        patch : str = row["Patch"]
        tournament : str = get_tournament_from_seriesId(seriesId)


        (data, _, _, _) = getData(seriesId, gameNumber)

        # Saving the draft into our CSV database

        # Checking if the database exists
        if os.path.exists(DATA_PATH + "drafts/draft_pick_order.csv") and os.path.exists(DATA_PATH + "drafts/draft_player_picks.csv"):
            draft_pick_order_df : pd.DataFrame = pd.read_csv(DATA_PATH + "drafts/draft_pick_order.csv", sep=";")
            draft_player_picks_df : pd.DataFrame = pd.read_csv(DATA_PATH + "drafts/draft_player_picks", sep=";")

            # Checking if the draft we want to save is already in our database
            if not(seriesId in draft_pick_order_df["SeriesId"].values and gameNumber in draft_pick_order_df["GameNumber"].values):
                if not(seriesId in draft_player_picks_df["SeriesId"].values and gameNumber in draft_player_picks_df["GameNumber"].values):
                    # Saving the draft into our csv database 
                    data.draftToCSV(DATA_PATH + "drafts/", new=True, patch=patch, seriesId=seriesId, tournament=tournament, gameNumber=gameNumber)
        else: 
            data.draftToCSV(DATA_PATH + "drafts/", new=False, patch=patch, seriesId=seriesId, tournament=tournament, gameNumber=gameNumber)

        # # Saving draftPickOrder to SQLite database
        # draft_pick_order_df : pd.DataFrame = pd.read_csv(DATA_PATH + "drafts/draft_pick_order.csv", sep=";")
        # draft_pick_order = draft_pick_order_df.loc[draft_pick_order_df["SeriesId"] == seriesId & 
        #                                            draft_pick_order_df["GameNumber"] == gameNumber]
        
        # draftPickOrder = DraftPickOrder(
        #     date = draft_pick_order["Date"],
        #     tournament = draft_pick_order["Tournament"],
        #     patch = draft_pick_order["Patch"],
        #     seriesId = draft_pick_order["SeriesId"],
        #     winner = draft_pick_order["Winner"],
        #     gameNumber = draft_pick_order["GameNumber"],

        #     bb1 = draft_pick_order["BB1"],
        #     bb2 = draft_pick_order["BB2"],
        #     bb3 = draft_pick_order["BB3"],
        #     bb4 = draft_pick_order["BB4"],
        #     bb5 = draft_pick_order["BB5"],

        #     bp1 = draft_pick_order["BP1"],
        #     bp2 = draft_pick_order["BP2"],
        #     bp3 = draft_pick_order["BP3"],
        #     bp4 = draft_pick_order["BP4"],
        #     bp5 = draft_pick_order["BP5"],


        #     rb1 = draft_pick_order["RB1"],
        #     rb2 = draft_pick_order["RB2"],
        #     rb3 = draft_pick_order["RB3"],
        #     rb4 = draft_pick_order["RB4"],
        #     rb5 = draft_pick_order["RB5"],

        #     rp1 = draft_pick_order["RP1"],
        #     rp2 = draft_pick_order["RP2"],
        #     rp3 = draft_pick_order["RP3"],
        #     rp4 = draft_pick_order["RP4"],
        #     rp5 = draft_pick_order["RP5"],
        # )
        # # Check if object already in database before saving it
        # if not(DraftPickOrder.objects.filter(seriesId = draftPickOrder.seriesId, gameNumber = draftPickOrder.gameNumner).exists()):
        #     draftPickOrder.save()

        # # Saving draftPlayerPick to SQLite database
        # draft_player_picks_df : pd.DataFrame = pd.read_csv(DATA_PATH + "drafts/draft_player_picks", sep=";")
        # draft_player_picks = draft_player_picks_df.loc[draft_player_picks_df["SeriesId"] == seriesId &
        #                                                draft_player_picks_df["GameNumber"] == gameNumber]
        
        # draftPlayerPick = DraftPlayerPick(
        #    date = draft_player_picks["Date"],
        #    tournament = draft_player_picks["Tournament"],
        #    patch = draft_player_picks["Patch"],
        #    seriesId = draft_player_picks["SeriesId"],
        #    summonnerName = draft_player_picks["SummonnerName"],
        #    championName = draft_player_picks["ChampionName"],
        #    role = draft_player_picks["Role"],
        #    gameNumber = draft_player_picks["GameNumber"],
        # )
        # # Check if object already in database before saving it
        # if not(DraftPlayerPick.objects.filter(seriesId = draftPlayerPick.seriesId, gameNumber = draftPlayerPick.gameNumber).exists()):
        #     draftPickOrder.save()

    return Response(status=status.HTTP_200_OK)
