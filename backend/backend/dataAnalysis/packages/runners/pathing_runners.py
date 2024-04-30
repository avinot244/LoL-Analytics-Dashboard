from dataAnalysis.packages.utils_stuff.utils_func import splitPlayerNameListPerTeam
from dataAnalysis.packages.utils_stuff.plots.densityPlot import getPositionsMultipleGames, getPositionsSingleGame, densityPlot
from dataAnalysis.packages.Parsers.Separated.Game.SeparatedData import SeparatedData
from dataAnalysis.packages.Parsers.EMH.Summary.SummaryData import SummaryData
from dataAnalysis.packages.utils_stuff.utils_func import getData, getSummaryData
from dataAnalysis.globals import DATA_PATH

from behaviorADC.models import *

import os
import matplotlib.pyplot as plt

def getDataPathing(game : dict, role : str):
    # Loading data of the game
    print("Loading game(s) data")
    
    # Getting global info of the game
    summaryData : SummaryData = getSummaryData(DATA_PATH + "games/bin/{}_ESPORTS_{}".format(game["seriesId"], game["gameNumber"]))
    (tempData, gameDuration, _, _) = getData(game["seriesId"], game["gameNumber"])

    
    splitList : list[int] = [90, 540, 900, 1925]
    if splitList[-1] > gameDuration:
        splitList[-1] = gameDuration
    else:
        splitList.append(gameDuration)
    
    splittedDataset : list[SeparatedData] = tempData.splitData(summaryData.gameDuration, splitList)
    if role == "Top":
        playerNameList = [[res.summonnerName] for res in BehaviorTop.objects.filter(seriesId__exact=game["seriesId"], gameNumber__exact=game["gameNumber"])]
    elif role == "Jungle":
        playerNameList = [[res.summonnerName] for res in BehaviorJungle.objects.filter(seriesId__exact=game["seriesId"], gameNumber__exact=game["gameNumber"])]
    elif role == "Mid":
        playerNameList = [[res.summonnerName] for res in BehaviorMid.objects.filter(seriesId__exact=game["seriesId"], gameNumber__exact=game["gameNumber"])]
    elif role == "ADC":
        playerNameList = [[res.summonnerName] for res in BehaviorADC.objects.filter(seriesId__exact=game["seriesId"], gameNumber__exact=game["gameNumber"])]
    elif role == "Support":
        playerNameList = [[res.summonnerName]for res in BehaviorSupport.objects.filter(seriesId__exact=game["seriesId"], gameNumber__exact=game["gameNumber"])]

    return splittedDataset, splitList, playerNameList
    # else:
    #     print("multiple games")
    #     data : list[list[SeparatedData]] = list()
    #     for game in gameList:

    #         summaryData : SummaryData = getSummaryData(DATA_PATH + "games/bin/{}_ESPORTS_{}".format(game["seriesId"], game["gameNumber"]))
    #         (tempData, gameDuration, _, _) = getData(game["seriesId"], game["gameNumber"])
    #         splitList : list[int] = [90, 540, 900, 1925]
    #         if splitList[-1] > gameDuration:
    #             splitList[-1] = gameDuration
    #         else:
    #             splitList.append(gameDuration)
    #         splittedDataset : list[SeparatedData] = tempData.splitData(summaryData.gameDuration, splitList)

    #         if role == "Top":
    #             playerNameList = [[res.summonnerName] for res in BehaviorTop.objects.filter(seriesId__exact=game["seriesId"], gameNumber__exact=game["gameNumber"])]
    #         elif role == "Jungle":
    #             playerNameList = [[res.summonnerName] for res in BehaviorTop.objects.filter(seriesId__exact=game["seriesId"], gameNumber__exact=game["gameNumber"])]
    #         elif role == "Mid":
    #             playerNameList = [[res.summonnerName] for res in BehaviorTop.objects.filter(seriesId__exact=game["seriesId"], gameNumber__exact=game["gameNumber"])]
    #         elif role == "ADC":
    #             playerNameList = [[res.summonnerName] for res in BehaviorTop.objects.filter(seriesId__exact=game["seriesId"], gameNumber__exact=game["gameNumber"])]
    #         elif role == "Support":
    #             playerNameList = [[res.summonnerName]for res in BehaviorTop.objects.filter(seriesId__exact=game["seriesId"], gameNumber__exact=game["gameNumber"])]


    #         data.append(splittedDataset)
        

def makeDensityPlot(game : dict,
                    playerNameList : list, 
                    data, 
                    splitList : list[int]):
    
    print("Plotting position density of game {} for players {}".format(game["seriesId"], playerNameList))
    if not(os.path.exists("{}/plots/Position/PositionDensity/{}_{}/".format(DATA_PATH, game["seriesId"], game["gameNumber"]))):
        os.makedirs("{}/plots/Position/PositionDensity/{}_{}/".format(DATA_PATH, game["seriesId"], game["gameNumber"]))
    save_path = "{}/plots/Position/PositionDensity/{}_{}/".format(DATA_PATH, game["seriesId"], game["gameNumber"])
        
    i = 0
    for split in data:
        graph_name = ""
        if i < len(splitList):
            # For team one
            if playerNameList[0]:
                graph_name = "{}_{}_blue_{}".format(playerNameList[0][0], splitList[i], game["seriesId"])
                participantPositions = getPositionsSingleGame(playerNameList[0], split)
                densityPlot(participantPositions, graph_name, save_path)

            # For team two
            if playerNameList[1]:
                graph_name = "{}_{}_red_{}".format(playerNameList[1][0], splitList[i], game["seriesId"])
                participantPositions = getPositionsSingleGame(playerNameList[1], split)
                densityPlot(participantPositions, graph_name, save_path)
        i += 1
    plt.close()
    