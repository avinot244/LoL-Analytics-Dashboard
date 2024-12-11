from tqdm import tqdm
import csv

from dataAnalysis.models import GameMetadata
from dataAnalysis.packages.Parsers.EMH.Summary.SummaryData import SummaryData
from dataAnalysis.packages.utils_stuff.utils_func import getSummaryData

query = GameMetadata.objects.all()

print("Deleting All objects")
for q in tqdm(query):
    q.delete()


with open("./databases/games/data_metadata_copy.csv", "r") as csv_copy:
    reader = csv.reader(csv_copy, delimiter=";")
    
    for line in tqdm(reader):
        
        summaryData : SummaryData = getSummaryData(seriesId, gameNumber)
        dragonBlueKills : int = summaryData.getObjectiveCount(0, "dragon")
        dragonRedKills : int = summaryData.getObjectiveCount(1, "dragon")
        krubsBlueKills : int = summaryData.getObjectiveCount(0, "horde")
        krubsRedKills : int = summaryData.getObjectiveCount(1, "horde")
        
        temp = (date, tournament, name, patch, seriesId, teamBlue, teamRed, winningTeam, gameNumber) = line        
        

        gameMetadata : GameMetadata = GameMetadata(
            date=date, 
            tournament=tournament, 
            name=name, 
            patch=patch, 
            seriesId=int(seriesId), 
            teamBlue=teamBlue, 
            teamRed=teamRed, 
            winningTeam=winningTeam, 
            gameNumber=gameNumber,
            dragonBlueKills=dragonBlueKills,
            dragonRedKills=dragonRedKills,
            krubsBlueKills=krubsBlueKills,
            krubsRedKills=krubsRedKills
        )
        gameMetadata.save()
        
        with open("./databases/games/data_metadata.csv", "a") as csv_out:
            writer = csv.writer(csv_out, delimiter=";")
            
            dataCSV = [
                date, 
                tournament, 
                date, 
                patch, 
                int(seriesId), 
                teamBlue, 
                teamRed, 
                winningTeam, 
                gameNumber, 
                dragonBlueKills, 
                dragonRedKills,
                krubsBlueKills,
                krubsRedKills
            ]
            
            writer.writerow(dataCSV)