from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from behaviorADC.models import BehaviorADC

from .globals import DATA_PATH, BLACKLIST
from .packages.api_calls.GRID.api_calls import *
from .utils import isGameDownloaded

import json
import pandas as pd

@api_view(['PATCH'])
def behavior_latest(request, rawTournamentList : str):

    if rawTournamentList.__contains__(','):
        wantedTournamentList : list = rawTournamentList.split(",")
        
        # Getting the list of tournament in our database
        tournamentList : list = list()
        queryTournamentList = BehaviorADC.objects.all()
        for res in queryTournamentList:
            tournamentList.append(res.tournament)
        df = pd.DataFrame({'tournaments': tournamentList})
        tournamentList = df['tournaments'].unique().tolist()

        # Testing if the tournament list are in our database
        for res in wantedTournamentList:
            if not(res in tournamentList):
                return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # Opening our tournament mapping json
        tournamentMapping : dict = None
        with open(DATA_PATH + "tournament_mapping.json", "r") as json_file:
            tournamentMapping = json.loads(json_file.read())


        # Mapping our wanted tournament to get the list of wanted ids
        wantedTournamentMapping : dict = dict()
        for wantedTournamentName in wantedTournamentList:
            for tournament_name, tournament_id  in tournamentMapping.items():
                if wantedTournamentName == tournament_name:
                    wantedTournamentMapping[tournament_name] = tournament_id
        
        
        for tournament_name, tournament_id in wantedTournamentMapping.items():
            print(tournament_id, tournament_name)
            seriesIdList = get_all_game_seriesId_tournament(tournament_id, 200)
            
            
            for seriesId in seriesIdList:
                if not(isGameDownloaded(seriesId)) and not(seriesId in BLACKLIST):
                    dlDict : dict = get_all_download_links(seriesId)
                    print("\tChecking game of seriesId :", seriesId)
                    i = 0
                    for downloadDict in dlDict['files']:
                        fileType = downloadDict["fileName"].split(".")[-1]
                        fileName = downloadDict["fileName"].split(".")[0]
                        print(fileName, fileName.split("_")[-1])

                        if fileType != "rofl" and downloadDict["status"] == "ready":
                            if i > 1:
                                # The first 2 files are global info about the Best-of
                                # We have 4 files per games
                                # We add 1 to start the gameNumber list at 1
                                gameNumber = (i-2)//4 + 1

                                path : str = DATA_PATH + "games/bin/" + "{}_{}_{}/".format(seriesId, "ESPORTS", gameNumber)
                                print("\t\tDownloading {} files".format(fileName))
                                download_from_link(downloadDict['fullURL'], fileName, path, fileType)

                            else:
                                for gameNumber in range(1, get_nb_games_seriesId(seriesId) + 1):
                                    path : str = DATA_PATH + "games/bin/" + "{}_{}_{}/".format(seriesId, "ESPORTS", gameNumber)
                                    print("\t\tDownloading {} files".format(fileName))
                                    download_from_link(downloadDict['fullURL'], fileName, path, fileType)
                        elif fileType == "rofl":
                            print("\t\twe don't download rofl file")
                        i += 1
                    # Save game metadata in csv and sqlite databases
                    
                    date = get_date_from_seriesId(seriesId)
                    name : str = "{}_ESPORTS_{}dataSeparatedRIOT".format(seriesId, fileName.split("_")[-1])
                    patch : str


        return Response(wantedTournamentMapping)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
