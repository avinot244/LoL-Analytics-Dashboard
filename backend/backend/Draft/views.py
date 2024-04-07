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
        # TODO: Check if we already have a csv db => check if draft already saved
        data.draftToCSV(DATA_PATH + "drafts/", new=True, patch=patch, seriesId=seriesId, tournament=tournament)

        # Saving draftPickOrder to SQLite database
        draft_pick_order_df : pd.DataFrame = pd.read_csv(DATA_PATH + "drafts/draft_pick_order.csv", sep=";")
        draft_pick_order = draft_pick_order_df.loc[draft_pick_order_df["SeriesId"] == seriesId]
        
        draftPickOrder = DraftPickOrder(
            date = draft_pick_order["Date"],
            tournament = draft_pick_order["Tournament"],
            patch = draft_pick_order["Patch"],
            seriesId = draft_pick_order["SeriesId"],
            winner = draft_pick_order["Winner"],

            bb1 = draft_pick_order["BB1"],
            bb2 = draft_pick_order["BB2"],
            bb3 = draft_pick_order["BB3"],
            bb4 = draft_pick_order["BB4"],
            bb5 = draft_pick_order["BB5"],

            bp1 = draft_pick_order["BP1"],
            bp2 = draft_pick_order["BP2"],
            bp3 = draft_pick_order["BP3"],
            bp4 = draft_pick_order["BP4"],
            bp5 = draft_pick_order["BP5"],


            rb1 = draft_pick_order["RB1"],
            rb2 = draft_pick_order["RB2"],
            rb3 = draft_pick_order["RB3"],
            rb4 = draft_pick_order["RB4"],
            rb5 = draft_pick_order["RB5"],

            rp1 = draft_pick_order["RP1"],
            rp2 = draft_pick_order["RP2"],
            rp3 = draft_pick_order["RP3"],
            rp4 = draft_pick_order["RP4"],
            rp5 = draft_pick_order["RP5"],
        )
        # Check if object already in database before saving it
        # if not(DraftPickOrder.objects.filter(seriesId = draftPickOrder.seriesId).exists()):
        #     draftPickOrder.save()
        # if not()

    return Response(status=status.HTTP_200_OK)
