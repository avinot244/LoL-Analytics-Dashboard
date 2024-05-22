from behaviorModels.models import BehaviorModelsMetadata
from dataAnalysis.globals import API_URL, DATA_PATH, factorsPerRole

from tqdm import tqdm
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from factor_analyzer.factor_analyzer import FactorAnalyzer
import pandas as pd
import numpy as np
from joblib import load



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
