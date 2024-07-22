import pandas as pd
df = pd.read_csv("./databases/drafts/champion_draft_stats.csv", sep=";")
tournament_list = []

for index, row in df.iterrows():
    if not(row["Tournament"] in tournament_list):
        tournament_list.append(row["Tournament"])
    
    
print(",".join(tournament_list))