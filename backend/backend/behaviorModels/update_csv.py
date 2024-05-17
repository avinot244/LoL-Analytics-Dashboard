from .models import BehaviorModelsMetadata
from dataAnalysis.globals import DATA_PATH, factorNamePerRole, factorsPerRole

import csv

selected_uuid : str = "976c4e70-ea03-11ee-ad17-00155da9b7d8"

query = BehaviorModelsMetadata.objects.all()
with open(DATA_PATH + "behavior/models/behaviorModels_metadata.csv", "a") as csv_file:   
    writer = csv.writer(csv_file, delimiter=";")
    for res in query:
        data = []
        data.append(res.uuid)
        data.append(res.modelType)
        data.append(res.modelName)
        data.append(res.role)
        data.append(res.kmo)
        data.append(res.tournamentDict)
        data.append(factorsPerRole[res.role])
        data.append(factorNamePerRole[res.role])
        data.append(str(res.uuid) == selected_uuid)
        writer.writerow(data)
