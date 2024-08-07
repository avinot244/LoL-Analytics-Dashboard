from dataAnalysis.packages.api_calls.DDragon.api_calls import get_champion_mapping_key, get_champion_mapping_key_reversed

def convertToChampionName(id : int, patch : str):
    if id > 0:
        return get_champion_mapping_key(patch)[id]
    else:
        return ""

def convertToChampionID(championName : str, patch : str):
    if championName != "":
        return get_champion_mapping_key_reversed(patch)[championName]
    else:
        return -1