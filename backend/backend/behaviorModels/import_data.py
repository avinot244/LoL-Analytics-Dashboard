import pandas as pd
from behaviorModels.models import BehaviorModelsMetadata

csv_file_path = "./databases/behavior/models/behaviorModels_metadata.csv"
df = pd.read_csv(csv_file_path, sep=";")

for index, row in df.iterrows():
    behaviorModelsMetadata = BehaviorModelsMetadata(
        uuid = row["uuid"],
        modelType = row["model_type"],
        modelName = row["model_name"],
        role = row["role"],
        kmo = row["kmo"],
        tournamentDict = row["tournament_dict"],
    )
    behaviorModelsMetadata.save()

print("CSV data has been loaded into the Django database.")