from dataAnalysis.packages.utils_stuff.utils_func import splitPlayerNameListPerTeam
from dataAnalysis.packages.utils_stuff.plots.densityPlot import getPositionsMultipleGames, getPositionsSingleGame, densityPlot
from dataAnalysis.packages.Parsers.Separated.Game.SeparatedData import SeparatedData
from dataAnalysis.packages.Parsers.EMH.Summary.SummaryData import SummaryData
from dataAnalysis.packages.utils_stuff.utils_func import getData, getSummaryData
from dataAnalysis.globals import DATA_PATH

import os

# def getDataPathing(yamlParser : YamlParser):
#     # Loading data of the game
#     print("Loading game(s) data")
    
#     if len(yamlParser.ymlDict['match']) == 1:
#         match = yamlParser.ymlDict['match'][0]
#         rootdir = yamlParser.ymlDict['brute_data'] + "{}".format(match)
#         # Getting global info of the game
#         summaryData : SummaryData = getSummaryData(rootdir)
#         (tempData, gameDuration, _, _) = getData(yamlParser, idx=0)

        
#         splitList : list[int] = [int(e) for e in yamlParser.ymlDict['split'].split(',')]
#         if splitList[-1] > gameDuration:
#             splitList[-1] = gameDuration
#         else:
#             splitList.append(gameDuration)
        
#         splittedDataset : list[SeparatedData] = tempData.splitData(summaryData.gameDuration, splitList)

#         playerNameList = yamlParser.ymlDict['players']

        

#         # TODO : assert if player names in the list are in the game

#         return splittedDataset, splitList, playerNameList
#     else:
#         print("multiple games")
#         i = 0
#         data : list[list[SeparatedData]] = list()
#         for matchName in yamlParser.ymlDict['match']:
#             rootdir = yamlParser.ymlDict['brute_data'] + matchName

#             summaryData : SummaryData = getSummaryData(rootdir)
#             (tempData, gameDuration, _, _) = getData(yamlParser, idx=i)
#             splitList : list[int] = [int(e) for e in yamlParser.ymlDict['split'].split(',')]
#             if splitList[-1] > gameDuration:
#                 splitList[-1] = gameDuration
#             else:
#                 splitList.append(gameDuration)
#             splittedDataset : list[SeparatedData] = tempData.splitData(summaryData.gameDuration, splitList)

#             playerNameList = yamlParser.ymlDict['players']

#             # TODO : assert if player names in the list are in the game

#             data.append(splittedDataset)
#             i += 1
        
#         return data, splitList, playerNameList

# def makeDensityPlot(seriesId : int,
#                     gameNumber : int,
#                     playerNameList : list[str], 
#                     data, 
#                     splitList : list[int]):
    

#     print("Plotting position density of game {} for players {}".format(seriesId, playerNameList))
#     if not(os.path.exists("{}/Position/PositionDensity/{}_{}/".format(DATA_PATH, seriesId, gameNumber))):
#         os.makedirs("{}/Position/PositionDensity/{}_{}/".format(DATA_PATH, seriesId, gameNumber))
#     save_path = "{}/Position/PositionDensity/{}_{}/".format(DATA_PATH, seriesId, gameNumber)
    
#     playerNameList = splitPlayerNameListPerTeam(data[0], playerNameList)
    
#     i = 0
#     for split in data:
#         graph_name = ""
#         if i < len(splitList):
#             # For team one
#             if playerNameList[0]:
#                 graph_name = "position_density_teamOne_{}_{}".format(splitList[i], yamlParser.ymlDict['match'][0])
#                 participantPositions = getPositionsSingleGame(playerNameList[0], split)
#                 densityPlot(participantPositions, graph_name, save_path)

#             # For team two
#             if playerNameList[1]:
#                 graph_name = "position_density_teamTwo_{}_{}".format(splitList[i], yamlParser.ymlDict['match'][0])
#                 participantPositions = getPositionsSingleGame(playerNameList[1], split)
#                 densityPlot(participantPositions, graph_name, save_path)
#         i += 1
    
    # if len(yamlParser.ymlDict['match']) > 1:

    #     print("Plotting position density of games {} for players {}".format(yamlParser.ymlDict['match'], playerNameList))
    #     if not(os.path.exists("{}/Position/PositionDensity/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0]))):
    #         os.makedirs("{}/Position/PositionDensity/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0]))
    #     save_path = "{}/Position/PositionDensity/{}/".format(yamlParser.ymlDict['save_path'], yamlParser.ymlDict['match'][0])

    #     for i in range(len(splitList)):
    #         # Formating the name of our plot
    #         nameListStr = ""
    #         for name in playerNameList:
    #             nameListStr += "_{}".format(name)
    #         graph_name = "position_density_{}{}".format(splitList[i], nameListStr)

    #         # Getting the data of all games for the according split and putting it into a single list
    #         tempData : list[SeparatedData] = list()
    #         for game in data:
    #             if i < len(game):
    #                 tempData.append(game[i])
    #         participantPositions = getPositionsMultipleGames(playerNameList, tempData)
    #         densityPlot(participantPositions, graph_name, save_path)