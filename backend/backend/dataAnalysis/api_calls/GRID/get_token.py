import requests
import pandas as pd
import json
import os

def get_token():
    with open("./behaviorADC/api_calls/GRID/token.json") as f:
        data = json.loads(f.read())
        df = pd.json_normalize(data)
        return df["key"][0]