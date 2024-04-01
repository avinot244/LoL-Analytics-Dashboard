import pandas as pd
import json

def get_token():
    with open("./dataAnalysis/packages/api_calls/GRID/token.json") as f:
        data = json.loads(f.read())
        df = pd.json_normalize(data)
        return df["key"][0]