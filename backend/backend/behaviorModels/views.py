from django.shortcuts import render

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from dataAnalysis.globals import DATA_PATH, ROLE_LIST, API_URL, factorsPerRole, factorNamePerRole

from .models import BehaviorModelsMetadata
from .serializers import BehaviorModelsMetadataSerializer
from .utils import saveToDatabase

import pandas as pd
import json
import requests
import uuid
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
from tqdm import tqdm
import re

from joblib import dump, load

from sklearn.preprocessing import RobustScaler, MinMaxScaler
from factor_analyzer.factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_kmo


@api_view(['GET'])
def get_all_models(request):
    queryResult = BehaviorModelsMetadata.objects.all()
    serializer = BehaviorModelsMetadataSerializer(queryResult, context={"request": request}, many=True)
    return Response(serializer.data)

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
    print(tournamentDict)

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
    header = [column for column in wantedDB.columns[7:]]
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
    saveToDatabase(model_id, model_name, role, "PCA", kmo, tournamentDict, factorsPerRole[role], factorNamePerRole[role], False)

    print("Model successfully saved to csv database")

    # Saving the model to our SQLite database
    behaviorModelsMetadata = BehaviorModelsMetadata(
        uuid = model_id,
        modelType = "PCA",
        modelName = model_name,
        role = role,
        kmo = kmo,
        tournamentDict = str(tournamentDict),
        nbFactors = factorsPerRole[role],
        factorsName = [],
        selected = False
    )

    behaviorModelsMetadata.save()

    print("Model successfully saved to SQLite database")
    serializer = BehaviorModelsMetadataSerializer(behaviorModelsMetadata, context={"request": request}, many=False)

    requests.patch(API_URL + "api/behaviorModels/generateLoadings/")

    return Response(serializer.data)

@api_view(['PATCH'])
def generate_loadings(request):
    query = BehaviorModelsMetadata.objects.all()

    for res in tqdm(query):
    
        if not os.path.exists(DATA_PATH + "behavior/models/loadings/{}/results_{}.png".format(res.uuid, res.role)):

            wantedModel = BehaviorModelsMetadata.objects.get(role__exact=res.role, uuid__exact=res.uuid)
            model_path : str = DATA_PATH + "behavior/models/bin/{}".format(wantedModel.modelName)
            factors = factorsPerRole[res.role]


            splittedDfList : list[pd.DataFrame] = list()
            dataSetSplit : dict = eval(wantedModel.tournamentDict)

            df = pd.read_csv(DATA_PATH + "behavior/behavior/behavior_{}.csv".format(res.role), sep=";")
            for tournament_name, nb_lines in dataSetSplit.items():
                temp : pd.DataFrame = df[df["Tournament"] == tournament_name]
                splittedDfList.append(temp.sample(nb_lines))

            wantedDB = pd.concat(splittedDfList)

            header = [column for column in wantedDB.columns[7:]]

            behavior = wantedDB[header]


            fig, axes = plt.subplots(ncols=1, figsize=(16, 7))
            
            fa_model : FactorAnalyzer = load(model_path + ".joblib")
            factor_matrix = fa_model.loadings_
            scaled_factor_matrix = []
            for line in factor_matrix:
                scaler : MinMaxScaler = MinMaxScaler().fit(np.abs(line).reshape(-1, 1))
                scaledLine = scaler.transform(np.abs(line).reshape(-1, 1))
                scaled_factor_matrix.append(scaledLine.reshape(1, -1).tolist()[0])

            scaled_factor_matrix = np.array(scaled_factor_matrix)

            #  Plot the data as a heat map
            im = axes.imshow(factor_matrix, cmap="RdBu_r", vmax=1, vmin=-1, aspect='auto')
            #  and add the corresponding value to the center of each cell
            for (i,j), z in np.ndenumerate(factor_matrix):
                
                axes.text(j, i, str(z.round(factors)), ha="center", va="center")
            #  Tell matplotlib about the metadata of the plot
            axes.set_yticks(np.arange(len(behavior.columns)))
            if axes.get_subplotspec().is_first_col():
                axes.set_yticklabels(behavior.columns)
            else:
                axes.set_yticklabels([])
            axes.set_title("Loading model {}".format(res.uuid))
            axes.set_xticks(np.arange(factors))
            axes.set_xticklabels(["Factor {}".format(i+1) for i in range(factors)])
            #  and squeeze the axes tight, to save space
            plt.tight_layout()
                
            #  and add a colorbar
            cb = fig.colorbar(im, ax=axes, location='right', label="loadings")
            if not(os.path.exists(DATA_PATH + "behavior/models/loadings/{}".format(res.uuid))):
                os.makedirs(DATA_PATH + "behavior/models/loadings/{}".format(res.uuid))
            
            plt.savefig(DATA_PATH + "behavior/models/loadings/{}/results_{}.png".format(res.uuid, res.role))
            plt.close()

    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
def deleteAllModelsMetadata(request):
    query = BehaviorModelsMetadata.objects.all()
    for res in query:
        res.delete()

    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def get_loading_matrix(request, uuid, role):
    if not(role in ROLE_LIST):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    temp_df = pd.read_csv(DATA_PATH + "behavior/models/behaviorModels_metadata.csv", sep=";")
    if not(uuid in temp_df["uuid"].unique().tolist()):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if not os.path.exists(DATA_PATH + "behavior/models/loadings/{}/results_{}.png".format(uuid, role)):

        wantedModel = BehaviorModelsMetadata.objects.get(role__exact=role, uuid__exact=uuid)
        model_path : str = DATA_PATH + "behavior/models/bin/{}".format(wantedModel.modelName)
        factors = factorsPerRole[role]


        splittedDfList : list[pd.DataFrame] = list()
        dataSetSplit : dict = eval(wantedModel.tournamentDict)

        df = pd.read_csv(DATA_PATH + "behavior/behavior/behavior_{}.csv".format(role), sep=";")
        for tournament_name, nb_lines in dataSetSplit.items():        
            temp : pd.DataFrame = df[df["Tournament"] == tournament_name]
            splittedDfList.append(temp.sample(nb_lines))

        wantedDB = pd.concat(splittedDfList)

        header = [column for column in wantedDB.columns[7:]]
        print(header)

        behavior = wantedDB[header]


        fig, axes = plt.subplots(ncols=1, figsize=(16, 7))
        
        fa_model : FactorAnalyzer = load(model_path + ".joblib")
        factor_matrix = fa_model.loadings_
        scaled_factor_matrix = []
        for line in factor_matrix:
            scaler : MinMaxScaler = MinMaxScaler().fit(np.abs(line).reshape(-1, 1))
            scaledLine = scaler.transform(np.abs(line).reshape(-1, 1))
            scaled_factor_matrix.append(scaledLine.reshape(1, -1).tolist()[0])

        scaled_factor_matrix = np.array(scaled_factor_matrix)

        #  Plot the data as a heat map
        im = axes.imshow(factor_matrix, cmap="RdBu_r", vmax=1, vmin=-1, aspect='auto')
        #  and add the corresponding value to the center of each cell
        for (i,j), z in np.ndenumerate(factor_matrix):
            
            axes.text(j, i, str(z.round(factors)), ha="center", va="center")
        #  Tell matplotlib about the metadata of the plot
        axes.set_yticks(np.arange(len(behavior.columns)))
        if axes.get_subplotspec().is_first_col():
            axes.set_yticklabels(behavior.columns)
        else:
            axes.set_yticklabels([])
        axes.set_title("Loading model {}".format(uuid))
        axes.set_xticks(np.arange(factors))
        axes.set_xticklabels(["Factor {}".format(i+1) for i in range(factors)])
        #  and squeeze the axes tight, to save space
        plt.tight_layout()
            
        #  and add a colorbar
        cb = fig.colorbar(im, ax=axes, location='right', label="loadings")
        if not(os.path.exists(DATA_PATH + "behavior/models/loadings/{}".format(uuid))):
            os.makedirs(DATA_PATH + "behavior/models/loadings/{}".format(uuid))
        
        plt.savefig(DATA_PATH + "behavior/models/loadings/{}/results_{}.png".format(uuid, role))
        
    with open(DATA_PATH + "behavior/models/loadings/{}/results_{}.png".format(uuid, role), "rb") as f:
        return HttpResponse(f.read(), content_type="image/png")
    
@api_view(['DELETE'])
def deleteModel(request, uuid : str, role : str):
    toDelete = BehaviorModelsMetadata.objects.get(uuid__exact=uuid, role__exact=role)
    df : pd.DataFrame = pd.read_csv(DATA_PATH + "behavior/models/behaviorModels_metadata.csv", sep=";")
    idx_delete : int = df[((df.uuid == str(toDelete.uuid)) & (df.role == toDelete.role))].index
    df.drop(idx_delete, inplace=True)
    os.remove(DATA_PATH + "behavior/models/behaviorModels_metadata.csv")
    df.to_csv(DATA_PATH + "behavior/models/behaviorModels_metadata.csv", sep=";", index=False)

    toDelete.delete()
    return Response(status=status.HTTP_200_OK)

@api_view(['PATCH'])
def setModelAsActive(request, uuid : str, role : str):
    previousModel = BehaviorModelsMetadata.objects.get(role__exact=role, selected__exact=True)
    previousModel.selected = False
    previousModel.save()


    model = BehaviorModelsMetadata.objects.get(uuid__exact=uuid, role__exact=role)
    model.selected = True
    model.save()

    df : pd.DataFrame = pd.read_csv(DATA_PATH + "behavior/models/behaviorModels_metadata.csv", sep=";")
    
    idx_selected : int = df[((df.uuid == str(model.uuid)) & (df.role == model.role))].index.to_list()[0]
    df.loc[idx_selected: idx_selected] = [model.uuid, model.modelType, model.modelName, model.role, model.kmo, model.tournamentDict, model.nbFactors, model.factorsName, model.selected]
    os.remove(DATA_PATH + "behavior/models/behaviorModels_metadata.csv")
    df.to_csv(DATA_PATH + "behavior/models/behaviorModels_metadata.csv", sep=";", index=False)

    return Response(status=status.HTTP_200_OK)

@api_view(['PATCH'])
def setFactorsName(request, uuid : str, role : str):
    factorsName_unicode = request.body.decode("utf-8")
    factorsName : list = json.loads(factorsName_unicode)

    model = BehaviorModelsMetadata.objects.get(uuid__exact=uuid, role__exact=role)
    model.factorsName = str(factorsName)
    model.save()

    df : pd.DataFrame = pd.read_csv(DATA_PATH + "behavior/models/behaviorModels_metadata.csv", sep=";")
    idx_selected : int = df[((df.uuid == str(model.uuid)) & (df.role == model.role))].index.to_list()[0]
    df.loc[idx_selected: idx_selected] = [model.uuid, model.modelType, model.modelName, model.role, model.kmo, model.tournamentDict, model.nbFactors, model.factorsName, model.selected]
    os.remove(DATA_PATH + "behavior/models/behaviorModels_metadata.csv")
    df.to_csv(DATA_PATH + "behavior/models/behaviorModels_metadata.csv", sep=";", index=False)

    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def getModel(request, role : str):
    model = BehaviorModelsMetadata.objects.get(role__exact=role, selected__exact=True)
    serializer = BehaviorModelsMetadataSerializer(model, context={"request": request}, many=False)
    return Response(serializer.data)


def searchRegion(regionList : list[str], tournament_name : str):

    for i in range(len(regionList)):
        x = re.search(regionList[i], tournament_name)
        
        if x != None:
            if i == len(regionList):
                return i-1
            else:
                return i
    return -1
        
@api_view(['GET'])
def getRegionSplit(request, uuid : str, role : str):
    regionList : list[str] = ["LCK", "LEC", "LCS"]
    model = BehaviorModelsMetadata.objects.get(role__exact=role, uuid__exact=uuid)
    tournamentDict : dict = json.loads(model.tournamentDict.replace("'", "\""))

    res : dict = {
        "LCK": 0,
        "LEC": 0,
        "LCS": 0,
        "MSI": 0,
        "Worlds": 0,
        "Other": 0
    }


    for tournament_name, amount in tournamentDict.items():
        
        idx = searchRegion(regionList, tournament_name)
        if amount > 0 and idx != -1:
            res[regionList[idx]] += amount
        elif amount > 0:
            res["Other"] += amount

    return Response(res)
