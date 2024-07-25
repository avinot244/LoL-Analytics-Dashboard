from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import requests

from Monitoring.packages.refresh_behavior.refresh_behavior_adc import refresh_behavior_adc
from Monitoring.packages.refresh_behavior.refresh_behavior_jungle import refresh_behavior_jungle
from Monitoring.packages.refresh_behavior.refresh_behavior_mid import refresh_behavior_mid
from Monitoring.packages.refresh_behavior.refresh_behavior_support import refresh_behavior_support
from Monitoring.packages.refresh_behavior.refresh_behavior_top import refresh_behavior_top

from Monitoring.packages.refresh_drafts.refresh_championDraftStats import refresh_championDraftStats
from Monitoring.packages.refresh_drafts.refresh_draftPickOrder import refresh_draftPickOrder
from Monitoring.packages.refresh_drafts.refresh_draftPlayerPick import refresh_draftPlayerPick
from Monitoring.packages.refresh_drafts.refresh_playerChampionPool import refresh_playerChampionPool
from Monitoring.packages.refresh_drafts.refresh_championBanStats import refresh_championBanStats

from Monitoring.packages.refresh_games.refresh_gameMetadata import refresh_gameMetadata

from dataAnalysis.globals import API_URL

@api_view(['PATCH'])
def refresh_db(request, dbName : str):
    if not(dbName in ["behavior", "drafts", "games"]):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if dbName == "behavior":
        print(f"{' Deleting All Behaviors ' :#^50}")
        requests.delete(API_URL + "api/behavior/deleteAll/") # Deleting all behaviors
        print(f"{' Importing ADC Behaviors ' :#^50}")
        refresh_behavior_adc()
        print(f"{' Importing Jungle Behaviors ' :#^50}")
        refresh_behavior_jungle()
        print(f"{' Importing Mid Behaviors ' :#^50}")
        refresh_behavior_mid()
        print(f"{' Importing Support Behaviors ' :#^50}")
        refresh_behavior_support()
        print(f"{' Importing Top Behaviors ' :#^50}")
        refresh_behavior_top()
    elif dbName == "drafts":
        print(f"{' Deleting Champion draft stats ' :#^50}")
        requests.delete(API_URL + "api/draft/championStats/deleteChampionGameStats/") # Deleting champion draft stats
        print(f"{' Deleting Draft pick order and player picks ' :#^50}")
        requests.delete(API_URL + "api/draft/delete/") # Deleting draft pick order and draft player picks
        print(f"{' Deleting Champion pools ' :#^50}")
        requests.delete(API_URL + "api/draft/playerStat/deleteAll/") # Deleting champion pools
        print(f"{' Deleting Champion ban stats' :#^50}")
        requests.delete(API_URL + "api/draft/championStats/deleteChampionBansStats/") # Deleting banned champs
        print(f"{' Importing Champion draft stats ' :#^50}")
        refresh_championDraftStats()
        print(f"{' Importing Draft pick order ' :#^50}")
        refresh_draftPickOrder()
        print(f"{' Importing Draft player picks ' :#^50}")
        refresh_draftPlayerPick()
        print(f"{' Importing Champion pools ' :#^50}")
        refresh_playerChampionPool()
        print(f"{' Importing Champion ban stats ' :#^50}")
        refresh_championBanStats()
    elif dbName == "games":
        print(f"{' Deleting All Game Metadata' :#^50}")
        requests.delete(API_URL + "api/dataAnalysis/deleteAllMeta/") # Deleting all game meta data
        print(f"{' Importing Game Metadata ' :#^50}")
        refresh_gameMetadata()
    
    return Response(status=status.HTTP_200_OK)

# Create your views here.
