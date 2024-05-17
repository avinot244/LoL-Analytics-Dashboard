from dataAnalysis.globals import DATA_PATH

import csv

def saveToDatabase(id : str, model_name : str, role : str, model_type : str, kmo : float, tournamentDict : dict, nbFactors : int, factorsName : list, selected : bool):
    with open(DATA_PATH + "behavior/models/behaviorModels_metadata.csv", "a") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        data = [id, model_type, model_name, role, kmo, str(tournamentDict), nbFactors, str(factorsName), selected]
        writer.writerow(data)