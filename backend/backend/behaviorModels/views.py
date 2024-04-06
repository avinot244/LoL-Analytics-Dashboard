from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from dataAnalysis.globals import DATA_PATH, ROLE_LIST, API_URL, factorsPerRole

from .models import BehaviorModelsMetadata
from .serializers import BehaviorModelsMetadataSerializer
from .utils import saveToDatabase

import pandas as pd
import json
import requests
import uuid

from joblib import dump

from sklearn.preprocessing import RobustScaler
from factor_analyzer.factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_kmo


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


@api_view(['POST'])
def compute_model(request, role):
    tournamentDict_unicode = request.body.decode("utf-8")
    tournamentDict : dict = json.loads(tournamentDict_unicode)

    if not(role in ROLE_LIST):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Checking if the tournaments in tournamentDict are in our database
    response = requests.get(
        API_URL + 'api/dataAnalysis/tournament/getList'
    )

    tournamentList : list = list()
    for tournament in response.json():
        tournamentList.append(tournament)
    
    flag : bool = True
    i : int = 0
    while (flag and i < len(list(tournamentDict.keys()))):
        if (tournamentDict[list(tournamentDict.keys())[i]] != 0):
            flag = flag and (list(tournamentDict.keys())[i] in tournamentList)
        i += 1
    
    if not(flag):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # Building the dataset on which the factor analysis model will be operated
    df = pd.read_csv(DATA_PATH + "behavior/behavior/behavior_{}.csv".format(role), sep=";")

    splittedDfList : list[pd.DataFrame] = list()

    for tournament_name, nb_lines in tournamentDict.items():
        temp : pd.DataFrame = df[df["Tournament"] == tournament_name]
        splittedDfList.append(temp.sample(nb_lines))
    
    wantedDB = pd.concat(splittedDfList)
    
    # Building our factor analysis model
    factors = factorsPerRole[role]
    header = [column for column in wantedDB.columns[6:]]
    behavior = wantedDB[header]

    X = RobustScaler().fit_transform(behavior)
    
    fa = FactorAnalyzer(n_factors=factors, rotation="varimax")
    fa = fa.fit(X)
    
    print("Model successfully computed")

    # Saving the model to our csv database
    model_id : str = uuid.uuid1()
    _, kmo = calculate_kmo(X)
    model_name : str = "PCA_model_{}_{}".format(role, model_id)
    s = dump(fa, DATA_PATH + "behavior/models/bin/" + model_name + ".joblib")
    saveToDatabase(model_id, model_name, role, "PCA", kmo, tournamentDict)

    print("Model successfully saved to csv database")

    # Saving the model to our SQLite database
    behaviorModelsMetadata = BehaviorModelsMetadata(
        uuid = model_id,
        modelType = "PCA",
        modelName = model_name,
        role = role,
        kmo = kmo,
        tournamentDict = str(tournamentDict)
    )
    behaviorModelsMetadata.save()

    print("Model successfully saved to SQLite database")
    return Response(BehaviorModelsMetadataSerializer(behaviorModelsMetadata).data)
