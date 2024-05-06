import requests
import json
import os
import zipfile
import io
import time

from .get_token import get_token


def get_last_games(amount : int, gameType : str) -> list[str]:
    assert gameType == "SCRIM" or gameType == "COMPETITIVE" or gameType == "ESPORTS"
    url = "https://api.grid.gg/central-data/graphql"
    body = """
    {
        allSeries(
            last: """ + str(amount) + """,
            filter: { 
                types: """ + str(gameType) + """
            }
            orderBy: ID
            orderDirection: DESC
        ) {
            totalCount
            pageInfo {
                hasPreviousPage
                hasNextPage
                startCursor
                endCursor
            }
            edges {
                node {
                    id
                }
            }
        }
    }
    """
    token = get_token()
    headers = {
        "x-api-key": token
    }
    response = requests.post(url=url,json={"query": body}, headers=headers)
    if response.status_code != 200:
        response.raise_for_status()
    
    result : dict = response.json()
    idList : list = list()
    edges = result["data"]["allSeries"]["edges"]
    for edge in edges:
       idList.append(edge["node"]["id"])
    
    return idList

def get_all_download_links(seriesId):
    url = "https://api.grid.gg/file-download/list/{}".format(seriesId)
    token = get_token()
    headers = {
        "x-api-key": token
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code != 200:
        response.raise_for_status()
    
    result : dict = response.json()
    return result
    
def download_from_link(url : str, fileName : str, path : str, fileType : str):
    if not(os.path.exists(path)):
        os.mkdir(path)

    token = get_token()
    headers = {
        "x-api-key": token
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code != 200:
        response.raise_for_status()

    if fileType == "json":
        with open(path + fileName + ".{}".format(fileType), "w") as file:
            json.dump(response.json(), file)
    
    if fileType == "jsonl":
        live_data = response.content.decode('utf-8').splitlines()

        i = 0
        if not(os.path.exists(path + "/Separated")):
            os.mkdir(path + "/Separated/")
        for event in live_data:
            with open(path + "/Separated/" + "{}.json".format(i), "w") as file:
                # event_data = json.loads(event)
                # json.dump(event, file)
                file.write(event)
            i += 1

    if fileType == "zip":
        z = zipfile.ZipFile(io.BytesIO(response.content))
        z.extractall(path=path + fileName)
        with open(path + fileName + "/" + fileName + ".jsonl", "r") as jsonFile :
            json_list = list(jsonFile)
            i = 0
            for json_str in json_list:
                result = json.loads(json_str)
                with open(path + fileName + "/{}.json".format(i), "w") as separatedJson:
                    json.dump(result, separatedJson)
                i += 1
            os.remove(path + fileName + "/" + fileName + ".jsonl")

def get_download_link_end_summary(seriesId : str, games : int):
    url = "https://api.grid.gg/file-download/end-state/riot/series/{}/games/{}/summary".format(seriesId, games)
    token = get_token()
    headers = {
        "x-api-key": token
    }
    response = requests.get(url=url, headers=headers)
    if response.status_code != 200:
        response.raise_for_status()
    
    with open("summary_{}_game_{}.json".format(seriesId, games), "w") as file:
        json.dump(response.json(), file)

def get_tournament_ids_from_page(cursor : str):
    url = "https://api.grid.gg/central-data/graphql"
    if cursor != "":
        body = """
                query Tournaments {
                tournaments(
                    last: 50
                    before: \"""" + cursor + """\"
                    filter: { titleId: "3" }) {
                    edges {
                        node {
                            name
                            startDate
                            endDate
                            id
                            externalLinks {
                                dataProvider {
                                    name
                                    description
                                }
                            }
                        }
                    }
                    totalCount
                    pageInfo {
                        endCursor
                        hasNextPage
                        hasPreviousPage
                        startCursor
                    }
                }
            }
        """
    else:
        body = """
                query Tournaments {
                tournaments(
                    last: 50
                    filter: { titleId: "3" }) {
                    edges {
                        node {
                            name
                            startDate
                            endDate
                            id
                            externalLinks {
                                dataProvider {
                                    name
                                    description
                                }
                            }
                        }
                    }
                    totalCount
                    pageInfo {
                        endCursor
                        hasNextPage
                        hasPreviousPage
                        startCursor
                    }
                }
            }
        """
    
    token = get_token()
    headers = {
        "x-api-key": token
    }

    response = requests.post(url=url,json={"query": body}, headers=headers)
    if response.status_code != 200:
        response.raise_for_status()
    
    result : dict = response.json()
    
    # Mapping tournament id
    tournamentMapping : dict = dict()
    for edge in result["data"]["tournaments"]["edges"]:
        node = edge["node"]
        tournamentMapping[node["name"]] = node["id"]
    
    # Computing the cursor for next page
    if result["data"]["tournaments"]["pageInfo"]["hasPreviousPage"]:
        cursorPreviousPage : str = result["data"]["tournaments"]["pageInfo"]["startCursor"]
    else:
        cursorPreviousPage : str = ""
    
    return tournamentMapping, cursorPreviousPage

def get_all_tournament_ids(fromCursor : str):
    if fromCursor == "":
        res, cursorPreviousPage = get_tournament_ids_from_page("")
    else:
        res, cursorPreviousPage = get_tournament_ids_from_page(fromCursor)
        
    # Forced to do max 40 API calls or API thinks we DDOS'ing the server x)
    while cursorPreviousPage != "":
        temp, cursorPreviousPage = get_tournament_ids_from_page(cursorPreviousPage)
        res.update(temp)
        time.sleep(1)
    
    return res
    
def get_all_game_seriesId_tournament(tournamentId : int, amount : int, fromCursor : str = ""):
    seriesIdList : list = list()

    nbPage : int = amount // 50
    nbGamesLeft : int = amount % 50

    if nbPage >= 1:
        if fromCursor == "":
            seriesIdList, cursorNextPage = get_game_seriesId_from_page_tournament("", 50, tournamentId)
        else:
            seriesIdList, cursorNextPage = get_game_seriesId_from_page_tournament(fromCursor, 50, tournamentId)
    else:
        if fromCursor == "":
            seriesIdList, cursorNextPage = get_game_seriesId_from_page_tournament("", nbGamesLeft, tournamentId)
        else:
            seriesIdList, cursorNextPage = get_game_seriesId_from_page_tournament(fromCursor, nbGamesLeft, tournamentId)    
    
    nbPage = nbPage - 1
    
    if nbPage > 1:
        i = 0
        while cursorNextPage != "" and i < nbPage:
            seriesId, cursorNextPage = get_game_seriesId_from_page_tournament(cursorNextPage, 50, tournamentId)
            for tempSeriesId in seriesId:
                seriesIdList.append(tempSeriesId)
            i += 1
        if cursorNextPage != "":
            seriesId, cursorNextPage = get_game_seriesId_from_page_tournament(cursorNextPage, nbGamesLeft, tournamentId)
            for tempSeriesId in seriesId:
                seriesIdList.append(tempSeriesId)
        return seriesIdList
    else:
        return seriesIdList

def get_game_seriesId_from_page_tournament(cursor : str, amount : int, tournamentId : int):
    url = "https://api.grid.gg/central-data/graphql"
    body = """
        {
            allSeries(
                first: """ + str(amount) + """
                after: \"""" + cursor + """\"
                filter: { 
                    titleId : 3,
                    tournamentId: """ + str(tournamentId) + """
                }
                orderBy: ID
                orderDirection: DESC
            ) {
                totalCount
                pageInfo {
                    hasPreviousPage
                    hasNextPage
                    startCursor
                    endCursor
                }
                edges {
                    node {
                        id
                        tournament {
                            id
                            endDate
                            logoUrl
                            name
                            nameShortened
                            startDate
                        }
                    }
                }
            }
        }
    """

    token = get_token()
    headers = {
        "x-api-key": token
    }
    response = requests.post(url=url,json={"query": body}, headers=headers)
    if response.status_code != 200:
        response.raise_for_status()
    
    result : dict = response.json()
    idList : list = list()
    edges = result["data"]["allSeries"]["edges"]
    for edge in edges:
       idList.append(edge["node"]["id"])
    
    # Computing the cursor for next page
    if result["data"]["allSeries"]["pageInfo"]["hasNextPage"]:
        cursorNextPage : str = result["data"]["allSeries"]["pageInfo"]["endCursor"]
    else:
        cursorNextPage : str = ""
    
    return idList, cursorNextPage

def get_nb_games_seriesId(seriesId : int):
    url = "https://api.grid.gg/live-data-feed/series-state/graphql"
    body = """
        {
            seriesState(id: \"""" + str(seriesId) + """\") {
                games {
                    sequenceNumber
                    id
                }
                id
            }
        }
    """

    token = get_token()
    headers = {
        "x-api-key": token
    }

    response = requests.post(url=url,json={"query": body}, headers=headers)
    if response.status_code != 200:
        response.raise_for_status()
    
    result : dict = response.json()

    if result["data"]:
        nbGames = len(result["data"]["seriesState"]["games"])
    
        return nbGames
    else:
        return -1

def get_tournament_from_seriesId(seriesId : int):
    url = "https://api.grid.gg/central-data/graphql"
    body = """
        query Series {
        series(id: \"""" + str(seriesId) + """\") {
            id
            tournament {
                name
                nameShortened
                id
            }
        }
    }
    """
    token = get_token()
    headers = {
        "x-api-key": token
    }
    response = requests.post(url=url,json={"query": body}, headers=headers)
    if response.status_code != 200:
        response.raise_for_status()
    
    result : dict = response.json()
    return result["data"]["series"]["tournament"]["name"]

def get_date_from_seriesId(seriesId : int):
    url = "https://api.grid.gg/central-data/graphql"
    body = """
        query Series {
            series(id: \"""" + str(seriesId) + """\") {
                id
                startTimeScheduled
                type
            }
        }
    """
    token = get_token()
    headers = {
        "x-api-key": token
    }
    response = requests.post(url=url,json={"query": body}, headers=headers)
    if response.status_code != 200:
        response.raise_for_status()
    
    result : dict = response.json()
    return result["data"]["series"]["startTimeScheduled"]

def get_dates_tournament(tournamentId : int):
    url = "https://api.grid.gg/central-data/graphql"
    body = """
        query Tournament {
            tournament(id: """ + tournamentId + """) {
                id
                endDate
                startDate
            }
        }
    """
    token = get_token()
    headers = {
        "x-api-key": token
    }
    response = requests.post(url=url,json={"query": body}, headers=headers)
    if response.status_code != 200:
        response.raise_for_status()
    
    result : dict = response.json()
    return result["data"]["tournament"]["startDate"], result["data"]["tournament"]["endDate"]