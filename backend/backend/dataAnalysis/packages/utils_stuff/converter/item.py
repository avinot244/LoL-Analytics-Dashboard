from dataAnalysis.packages.api_calls.DDragon.api_calls import get_item_mapping_key

def convertToItemName(id : int):
    return get_item_mapping_key()[id]
