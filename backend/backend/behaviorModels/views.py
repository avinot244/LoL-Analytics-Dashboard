from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from dataAnalysis.globals import DATA_PATH, ROLE_LIST

from .models import BehaviorModelsMetadata
from .serializers import BehaviorModelsMetadataSerializer

import pandas as pd

@api_view(['GET'])
def get_best_model(request, role):
    if not(role in ROLE_LIST):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    queryResult = BehaviorModelsMetadata.objects.filter(role__exact=role).order_by("-kmo")[:1]
    serializer = BehaviorModelsMetadataSerializer(queryResult, context={"request": request}, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_model(request, uuid, role):
    if not(role in ROLE_LIST):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    df = pd.read_csv(DATA_PATH + "behavior/models/behaviorModels_metadata.csv", sep=";")
    if not(uuid in df["uuid"].unique().tolist()):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    queryResult = BehaviorModelsMetadata.objects.filter(role__exact=role, uuid__exact=uuid)
    serializer = BehaviorModelsMetadataSerializer(queryResult, context={"request": request}, many=True)
    return Response(serializer.data)


