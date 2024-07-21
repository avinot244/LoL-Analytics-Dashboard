from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from Monitoring.packages.refresh_behavior.refresh_behavior_adc import refresh_behavior_adc
from Monitoring.packages.refresh_behavior.refresh_behavior_jungle import refresh_behavior_jungle
from Monitoring.packages.refresh_behavior.refresh_behavior_mid import refresh_behavior_mid
from Monitoring.packages.refresh_behavior.refresh_behavior_support import refresh_behavior_support
from Monitoring.packages.refresh_behavior.refresh_behavior_top import refresh_behavior_top

from Monitoring.packages.refresh_drafts.refresh_championDraftStats import refresh_championDraftStats
from Monitoring.packages.refresh_drafts.refresh_draftPickOrder import refresh_draftPickOrder
from Monitoring.packages.refresh_drafts.refresh_draftPlayerPick import refresh_draftPlayerPick
from Monitoring.packages.refresh_drafts.refresh_playerChampionPool import refresh_playerChampionPool

from Monitoring.packages.refresh_games.refresh_gameMetadata import refresh_gameMetadata

@api_view(['PATCH'])
def refresh_db(request, dbName : str):
    if not(dbName in ["behavior", "drafts", "games"]):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if dbName == "behavior":
        refresh_behavior_adc()
        refresh_behavior_jungle()
        refresh_behavior_mid()
        refresh_behavior_support()
        refresh_behavior_top()
    elif dbName == "drafts":
        refresh_championDraftStats()
        refresh_draftPickOrder()
        refresh_draftPlayerPick()
        refresh_playerChampionPool()
    elif dbName == "games":
        refresh_gameMetadata()
    
    return Response(status=status.HTTP_200_OK)

# Create your views here.
