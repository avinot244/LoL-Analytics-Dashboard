from django.db import models

class DraftPickOrder(models.Model):
    date = models.DateField("Date")
    tournament = models.CharField("Tournament", max_length=240)
    patch = models.CharField("Patch", max_length=240)
    seriesId = models.IntegerField("SeriesId")
    winner = models.IntegerField("Winner")
    gameNumner = models.IntegerField("GameNumber")
    teamBlue = models.CharField("teamBlue", max_length=240)
    teamRed = models.CharField("teamRed", max_length=240)

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
    date = models.DateField("Date")
    tournament = models.CharField("Tournament", max_length=240)
    patch = models.CharField("Patch", max_length=240)
    seriesId = models.IntegerField("SeriesId")
    sumonnerName = models.CharField("SumonnerName", max_length=240)
    championName = models.CharField("ChampionName", max_length=240)
    role = models.CharField("Role", max_length=240)
    gameNumber = models.IntegerField("GameNumber")

class ChampionDraftStats(models.Model):
    championName = models.CharField("ChampionName", max_length=240)
    patch = models.CharField("Patch", max_length=240)
    tournament = models.CharField("Tournament", max_length=240)
    side = models.CharField("Side", max_length=240)
    winRate = models.FloatField("WinRate")
    globalPickRate = models.FloatField("GlobalPickRate")
    pickRate1Rota = models.FloatField("PickRate1Rota")
    pickRate2Rota = models.FloatField("PickRate2Rota")
    globalBanRate = models.FloatField("GlobalBanRate")
    banRate1Rota = models.FloatField("BanRate1Rota")
    banRate2Rota = models.FloatField("BanRate2Rota")
    mostPopularPickOrder = models.IntegerField("MostPopularPickOrder")
    blindPick = models.FloatField("BlindPick")
    mostPopularRole = models.CharField("MostPopularRole", max_length=240)
    
class ChampionBanStats(models.Model):
    # We only take champions that have a pickrate of 0% and a banrate greater than 0%
    championName = models.CharField("ChampionName", max_length=240)
    patch = models.CharField("Patch", max_length=240)
    tournament = models.CharField("Tournament", max_length=240)
    side = models.CharField("Side", max_length=240)

class ChampionPool(models.Model):
    summonnerName = models.CharField("SummonnerName", max_length=240)
    championName = models.CharField("ChampionName", max_length=240)
    tournament = models.CharField("Tournament", max_length=240)
    globalPickRate = models.FloatField("GlobalPickRate")
    winRate = models.FloatField("WinRate")
    nbGames = models.IntegerField("NbGames")
    kda = models.FloatField("KDA")


