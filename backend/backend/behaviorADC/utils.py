from dataAnalysis.globals import DATA_PATH, factorsPerRole
from behaviorModels.models import BehaviorModelsMetadata

import pandas as pd
from factor_analyzer.factor_analyzer import FactorAnalyzer
from joblib import load

def getDataBase(role : str, summonnerName : str, wantedTournamentList : list) -> pd.DataFrame:
    df : pd.DataFrame = pd.read_csv(DATA_PATH + "behavior/behavior/behavior_{}.csv".format(role), sep=";")

    wantedDB : pd.DataFrame = df[df["SummonnerName"].isin([summonnerName])
                                 & df["Tournament"].isin(wantedTournamentList)]

    return wantedDB

def getFAModel(behaviorModelsMetadata : BehaviorModelsMetadata) -> FactorAnalyzer:
    model_path : str = DATA_PATH + "behavior/models/bin/{}.joblib".format(behaviorModelsMetadata.modelName)
    fa : FactorAnalyzer = load(model_path)
    return fa
    
def project(database : pd.DataFrame, model : FactorAnalyzer, role : str):
    # Scaling database
    metadataBehavior = database[database.columns[:6]]

    # Building our transformed database from the model
    transformed_database_content : list = list()
    for i in range(len(database)):
        row = model.transform(database[database.columns[6:]][i:i+1]).tolist()[0]
        temp = metadataBehavior.iloc[i].to_list() + row
        transformed_database_content.append(temp)
    

    columnsTransformed = [column for column in database.columns[:6]] + ["Factor_{}".format(i+1) for i in range(factorsPerRole[role])]
    transformed_database : pd.DataFrame = pd.DataFrame(transformed_database_content, columns=columnsTransformed)
    return transformed_database

def scaleDatabase(database : pd.DataFrame, scaler):
    database_scaled = pd.DataFrame(scaler.transform(database[database.columns[6:]]), columns = database.columns[6:])
    data : list = list()
    for i in range(len(database_scaled)):
        data.append(database[database.columns[:6]].iloc[i].to_list() + database_scaled.iloc[i].to_list())
    database_scaled = pd.DataFrame(data, columns = database.columns)
    return database_scaled