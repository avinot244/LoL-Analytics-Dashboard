import pandas as pd
from dataAnalysis.models import GameMetadata
import requests

from dataAnalysis.globals import DATA_PATH, BLACKLIST
from dataAnalysis.packages.api_calls.GRID.api_calls import *
from dataAnalysis.utils import isGameDownloaded, convertDate, checkSeries, getNbGamesSeries, checkFiles
from dataAnalysis.packages.utils_stuff.utils_func import getData, getSummaryData
from dataAnalysis.packages.Parsers.EMH.Summary.SummaryDataGrid import SummaryDataGrid

def getTeamName(df, seriesId, gameNumber, side):
    try:
        if side == 0:
            return df[(df['SeriesId'] == seriesId) & (df['gameNumber'] == gameNumber)]['teamBlue'].iloc[0]
        elif side == 1:
            return df[(df['SeriesId'] == seriesId) & (df['gameNumber'] == gameNumber)]['teamRed'].iloc[0]
    except Exception as e:
        print(seriesId, gameNumber, e)


with open("databases/games/data_metadata_copy.csv", "r") as f:
    df = pd.read_csv(f, sep=";")
data_tuples = list(df['SeriesId'].unique().tolist())

# data_tuples = [seriesId for seriesId in data_tuples if seriesId == 2682786]

print(data_tuples)

# allMetadata = GameMetadata.objects.all()
# for o in allMetadata:
#     o.delete()

for seriesId in data_tuples:
    if not(str(seriesId) in BLACKLIST) and not(GameMetadata.objects.filter(seriesId__exact=seriesId).count() > 0):
        try:
            dlDict : dict = get_all_download_links(seriesId)
        
            i = 0
            if checkSeries(dlDict['files']) and checkFiles(dlDict['files']):
                nbGames = getNbGamesSeries(dlDict['files'])
                print("\tChecking games of seriesId : {} {} games".format(seriesId, nbGames))
                for downloadDict in dlDict['files']:
                    fileType = downloadDict["fileName"].split(".")[-1]
                    fileName = downloadDict["fileName"].split(".")[0]
                    if i > 1 :
                        gameNumber = int(downloadDict["id"].split("-")[-1])
                    
                    if fileType != "rofl" and downloadDict["status"] == "ready":
                        if i > 1:
                            # The first 2 files are global info about the Best-of
                            # We have 3 files per games
                            # We add 1 to start the gameNumber at 1
                            # gameNumber = (i-2)//3 + 1
                            date = convertDate(get_date_from_seriesId(seriesId))
                            if not(isGameDownloaded(int(seriesId), gameNumber)) and gameNumber <= nbGames:

                                path : str = DATA_PATH + "games/bin/" + "{}_{}_{}/".format(seriesId, "ESPORTS", gameNumber)
                                print("\t\tDownloading {} files {}".format(fileName, gameNumber))
                                download_from_link(downloadDict['fullURL'], fileName, path, fileType)

                        else:
                            for gameNumber in range(1, nbGames + 1):
                                if not(isGameDownloaded(int(seriesId), gameNumber)):
                                    path : str = DATA_PATH + "games/bin/" + "{}_{}_{}/".format(seriesId, "ESPORTS", gameNumber)
                                    print("\t\tDownloading {} info".format(fileName))
                                    download_from_link(downloadDict['fullURL'], fileName, path, fileType)
                    elif fileType == "rofl":
                        print("\t\twe don't download rofl file")
                    i += 1

                # Save game metadata in csv and sqlite databases
                
                print("Saving to database ({} games)".format(nbGames))
                for gameNumberIt in range(1, nbGames + 1):
                    date = convertDate(get_date_from_seriesId(seriesId))
                    
                    if not(isGameDownloaded(int(seriesId), gameNumberIt)):
                        # print("saving to db")
                        # Getting relative information about the game
                        teamBlue = getTeamName(df, seriesId, gameNumberIt, 0)
                        teamRed = getTeamName(df, seriesId, gameNumberIt, 1)
                        (data, gameDuration, _, _) = getData(int(seriesId), gameNumberIt, date, _teamBlue=teamBlue, _teamRed=teamRed)
                        summaryDataGrid : SummaryDataGrid = getSummaryData(seriesId, gameNumber, "grid")
                        # Saving game metadata to SQLite datbase
                        gameMetadata : GameMetadata = GameMetadata(
                            date=date, 
                            tournament=get_tournament_from_seriesId(seriesId), 
                            name="{}_ESPORTS_{}dataSeparatedRIOT".format(seriesId, gameNumberIt), 
                            patch=data.patch, 
                            seriesId=seriesId, 
                            teamBlue=teamBlue, 
                            teamRed=teamRed, 
                            winningTeam=data.winningTeam, 
                            gameNumber=gameNumberIt,
                            gameDuration=gameDuration,
                            dragonBlueKills=summaryDataGrid.getDrakeCount(0),
                            dragonRedKills=summaryDataGrid.getDrakeCount(1),
                            voidGrubsBlueKills=summaryDataGrid.getGrubsCount(0),
                            voidGrubsRedKills=summaryDataGrid.getGrubsCount(1),
                            heraldBlueKills=data.getHeraldKills(0),
                            heraldRedKills=data.getHeraldKills(1),
                            baronBlueKills=data.getBaronKills(0),
                            baronRedKills=data.getBaronKills(1),
                            firstBlood=data.getFirstBlood(),
                            firstTower=data.getFirstTower(),
                            turretBlueKills=data.getTurretKills(0),
                            turretRedKills=data.getTurretKills(1),
                        )
                        gameMetadata.save()
                        print(f"Game {seriesId} {gameNumberIt} saved")
                    else :
                        print("game already downloaded")
            else:
                print("Game doesn't have the necessary files")
        except requests.exceptions.HTTPError as e:
            print(e)