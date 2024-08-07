import requests

def get_champion_mapping_key(patch : str):
    response = requests.get(
        'https://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json'.format(patch)
    )

    if response.status_code != 200:
        response.raise_for_status()
    res : dict = dict()
    
    for championName, data in response.json()['data'].items():
        res[int(data['key'])] = championName
    return res

def get_champion_mapping_key_reversed(patch : str):
    response = requests.get(
        'https://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json'.format(patch)
    )

    if response.status_code != 200:
        response.raise_for_status()
    res : dict = dict()
    for championName, data in response.json()['data'].items():
        
        res[championName] = int(data['key'])
    return res

def get_item_mapping_key():
    response = requests.get(
        'https://ddragon.leagueoflegends.com/cdn/14.13.1/data/en_US/item.json'
    )

    if response.status_code != 200:
        response.raise_for_status()

    res : dict = dict()
    for itemKey, data in response.json()['data'].items():
        res[itemKey] = data['name']
    
    return res