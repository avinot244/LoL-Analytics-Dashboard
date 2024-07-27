from behaviorModels.models import BehaviorModelsMetadata
from dataAnalysis.globals import ROLE_LIST, DATA_PATH
from behaviorADC.utils import compute, getFAModel, project, scaleDatabase

# header_offset = 8

from factor_analyzer.factor_analyzer import FactorAnalyzer
from sklearn.preprocessing import StandardScaler
import pandas as pd
from tqdm import tqdm

# 1 Transform dataset according to the active model
for role in tqdm(ROLE_LIST):
    # Getting the dataset and the model
    behaviorModelMetadata = BehaviorModelsMetadata.objects.get(role__exact=role, modelType__exact="PCA", selected__exact=True)
    df = pd.read_csv(DATA_PATH + "behavior/behavior/behavior_{}.csv".format(role), sep=";")
    fa_model : FactorAnalyzer = getFAModel(behaviorModelMetadata)
    df = df.loc[df['Tournament'] != "League of Legends Scrims"] # Excluding the scrims

    # Transform the wanted database
    df_transformed : pd.DataFrame = project(df, fa_model, role, 7) 
    
    # Getting the scaler
    scaler : StandardScaler = StandardScaler()
    scaler.fit(df_transformed[df_transformed.columns[7:]])
    
    
    df_scaled : pd.DataFrame = scaleDatabase(df_transformed, scaler, 7)
    df_scaled.to_csv(DATA_PATH + "behavior/behavior/behavior_{}_transformed.csv".format(role), index=False)
    
