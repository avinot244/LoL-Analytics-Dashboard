import pandas as pd
from dataAnalysis.models import GameMetadata

csv_file_path : str = "./databases/games/data_metadata.csv"
df = pd.read_csv(csv_file_path, sep=";")

for index, row in df.iterrows():
    gameMetadata = GameMetadata(
        date = row["Date"],
        name = row["Name"],
        patch = row["Patch"],
        seriesId = row["SeriesId"],
        teamBlue = row["teamBlue"],
        teamRed = row["teamRed"],
        winningTeam = row["winningTeam"],
    )
    gameMetadata.save()

print("CSV data has been loaded into the Django database.")