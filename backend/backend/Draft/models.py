from django.db import models

# "Date", "Patch", "SeriesId", "Winner", "BB1", "BB2", "BB3", "BB4", "BB5", "BP1", "BP2", "BP3", "BP4", "BP5", "RB1", "RB2", "RB3", "RB4", "RB5", "RP1", "RP2", "RP3", "RP4", "RP5"

class DraftPickOrder(models.Model):
    date = models.CharField("Date", max_length=240)
    patch = models.CharField("Patch", max_length=240)
    seriesId = models.IntegerField("SeriesId")
    winner = models.IntegerField("Winner")

    bb1 = models.CharField("BB1", max_length=240)
    bb2 = models.CharField("BB2", max_length=240)
    bb3 = models.CharField("BB3", max_length=240)
    bb4 = models.CharField("BB4", max_length=240)
    bb5 = models.CharField("BB5", max_length=240)

    bp1 = models.CharField("BP1", max_length=240)
    bp2 = models.CharField("BP3", max_length=240)
    bp3 = models.CharField("BP3", max_length=240)
    bp4 = models.CharField("BP4", max_length=240)
    bp5 = models.CharField("BP5", max_length=240)


    rb1 = models.CharField("RB1", max_length=240)
    rb2 = models.CharField("RB3", max_length=240)
    rb3 = models.CharField("RB3", max_length=240)
    rb4 = models.CharField("RB4", max_length=240)
    rb5 = models.CharField("RB5", max_length=240)

    rp1 = models.CharField("RP1", max_length=240)
    rp2 = models.CharField("RP3", max_length=240)
    rp3 = models.CharField("RP3", max_length=240)
    rp4 = models.CharField("RP4", max_length=240)
    rp5 = models.CharField("RP5", max_length=240)

class DraftPlayerPick(models.Model):
    date = models.CharField("Date", max_length=240)
    patch = models.CharField("Patch", max_length=240)
    seriesId = models.IntegerField("SeriesId")
    sumonnerName = models.CharField("SumonnerName", max_length=240)
    championName = models.CharField("ChampionName", max_length=240)
    role = models.CharField("Role", max_length=240)

