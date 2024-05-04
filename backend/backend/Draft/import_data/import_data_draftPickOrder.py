import pandas as pd
from ..models import DraftPickOrder

csv_draft_pick_order : str = "./databases/drafts/draft_pick_order.csv"

df_draft_pick_order : pd.DataFrame = pd.read_csv(csv_draft_pick_order, sep=";")
for index, row in df_draft_pick_order.iterrows():
    draftPickOrder = DraftPickOrder(
        date = row["Date"],
        tournament = row["Tournament"],
        patch = row["Patch"],
        seriesId = row["SeriesId"],
        winner = row["Winner"],
        gameNumner = row["GameNumber"],
        teamBlue = row["teamBlue"],
        teamRed = row["teamRed"],
        bb1 = row["BB1"],
        bb2 = row["BB2"],
        bb3 = row["BB3"],
        bb4 = row["BB4"],
        bb5 = row["BB5"],
        bp1 = row["BP1"],
        bp2 = row["BP2"],
        bp3 = row["BP3"],
        bp4 = row["BP4"],
        bp5 = row["BP5"],
        rb1 = row["RB1"],
        rb2 = row["RB2"],
        rb3 = row["RB3"],
        rb4 = row["RB4"],
        rb5 = row["RB5"],
        rp1 = row["RP1"],
        rp2 = row["RP2"],
        rp3 = row["RP3"],
        rp4 = row["RP4"],
        rp5 = row["RP5"]
    )
    if not(DraftPickOrder.objects.filter(
        date = row["Date"],
        tournament = row["Tournament"],
        patch = row["Patch"],
        seriesId = row["SeriesId"],
        winner = row["Winner"],
        gameNumner = row["GameNumber"],
        teamBlue = row["teamBlue"],
        teamRed = row["teamRed"],
        bb1 = row["BB1"],
        bb2 = row["BB2"],
        bb3 = row["BB3"],
        bb4 = row["BB4"],
        bb5 = row["BB5"],
        bp1 = row["BP1"],
        bp2 = row["BP2"],
        bp3 = row["BP3"],
        bp4 = row["BP4"],
        bp5 = row["BP5"],
        rb1 = row["RB1"],
        rb2 = row["RB2"],
        rb3 = row["RB3"],
        rb4 = row["RB4"],
        rb5 = row["RB5"],
        rp1 = row["RP1"],
        rp2 = row["RP2"],
        rp3 = row["RP3"],
        rp4 = row["RP4"],
        rp5 = row["RP5"]).count() > 0):
        
        draftPickOrder.save()