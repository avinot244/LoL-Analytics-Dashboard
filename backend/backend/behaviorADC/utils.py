from dataAnalysis.globals import DATA_PATH, factorsPerRole
from behaviorModels.models import BehaviorModelsMetadata

import pandas as pd
from factor_analyzer.factor_analyzer import FactorAnalyzer
from sklearn.preprocessing import StandardScaler
from joblib import load

def getDataBase(role : str, summonnerName : str, wantedTournament : str) -> pd.DataFrame:
    df : pd.DataFrame = pd.read_csv(DATA_PATH + "behavior/behavior/behavior_{}.csv".format(role), sep=";")

    wantedDB : pd.DataFrame = df[df["SummonnerName"].isin([summonnerName])
                                 & df["Tournament"].isin([wantedTournament])]

    return wantedDB

def getFAModel(behaviorModelsMetadata : BehaviorModelsMetadata) -> FactorAnalyzer:
    model_path : str = DATA_PATH + "behavior/models/bin/{}.joblib".format(behaviorModelsMetadata.modelName)
    fa : FactorAnalyzer = load(model_path)
    return fa
    
def project(database : pd.DataFrame, model : FactorAnalyzer, role : str, header_offset : int):
    # Scaling database
    metadataBehavior = database[database.columns[:header_offset]]
    # Building our transformed database from the model
    transformed_database_content : list = list()
    for i in range(len(database)):
        row = model.transform(database[database.columns[header_offset:]][i:i+1]).tolist()[0]
        temp = metadataBehavior.iloc[i].to_list() + row
        transformed_database_content.append(temp)
    

    columnsTransformed = [column for column in database.columns[:header_offset]] + ["Factor_{}".format(i+1) for i in range(factorsPerRole[role])]
    transformed_database : pd.DataFrame = pd.DataFrame(transformed_database_content, columns=columnsTransformed)
    return transformed_database

def scaleDatabase(database : pd.DataFrame, scaler, header_offset : int):
    database_scaled = pd.DataFrame(scaler.transform(database[database.columns[header_offset:]]), columns = database.columns[header_offset:])
    data : list = list()
    for i in range(len(database_scaled)):
        data.append(database[database.columns[:header_offset]].iloc[i].to_list() + database_scaled.iloc[i].to_list())
    database_scaled = pd.DataFrame(data, columns = database.columns)
    return database_scaled

def compute(wantedDB : pd.DataFrame, uuid : str, tournamentDict : dict, header_offset : int) -> pd.DataFrame:
    # Getting the fa model
    behaviorModelsMetadata = BehaviorModelsMetadata.objects.get(uuid__exact=uuid, modelType__exact="PCA", role__exact="ADC")
    fa_model : FactorAnalyzer = getFAModel(behaviorModelsMetadata)
    transformed_wantedDB : pd.DataFrame = project(wantedDB, fa_model, "ADC", header_offset) # Transform the wanted database
    
    # Scaling the wantedDB
    scaler : StandardScaler = StandardScaler()
    df : pd.DataFrame = pd.read_csv(DATA_PATH + "behavior/behavior/behavior_ADC.csv", sep=";")
    transformed_scaled_df : pd.DataFrame = project(df, fa_model, "ADC", 6)
    database_for_scaler = transformed_scaled_df[transformed_scaled_df["Tournament"].isin([tournamentDict["comparison"]])]
    scaler.fit(database_for_scaler[database_for_scaler.columns[6:]])

    # Scaling the transformed_wantedDB with the same scaler used when scaling the transformed database 
    # used when building the FactorAnalysis model
    transformed_wantedDB_scaled : pd.DataFrame = scaleDatabase(transformed_wantedDB, scaler, header_offset)
    return transformed_wantedDB_scaled