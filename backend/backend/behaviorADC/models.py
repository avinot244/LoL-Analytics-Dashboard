from django.db import models

class BehaviorTop(models.Model):
    date = models.DateField("Date")
    tournament = models.CharField("Tournament", max_length=240)
    matchId = models.CharField("MatchId", max_length=240)
    seriesId = models.IntegerField("SeriesId")
    patch = models.CharField("Patch", max_length=240)
    gameNumber = models.IntegerField("GameNumber")
    summonnerName = models.CharField("SummonnerName", max_length=240)
    xpd15 = models.IntegerField("XPD@15")
    gd15 = models.IntegerField("GD@15")
    csMin = models.FloatField("CS/Min")
    kills = models.IntegerField("Kills")
    deaths = models.IntegerField("Deaths")
    assists = models.IntegerField("Assists")
    kp = models.FloatField("KP%")
    wardPlaced = models.IntegerField("WardPlaced")
    dpm = models.FloatField("Damage/Min")
    totalDamageDealtToBuilding = models.FloatField("TotalDamageDealtToBuilding")
    totalDamageDealtToObjectives = models.FloatField("TotalDamageDealtToObjectives")
    jungleProximity = models.FloatField("JungleProximity")
    topLanePresence = models.FloatField("TopLanePresence")
    jungleAllyTopPresence = models.FloatField("jungleAllyTopPresence")
    jungleEnemyTopPresence = models.FloatField("JungleEnemyTopPresence")
    riverTopPresence = models.FloatField("riverTopPresence")


class BehaviorJungle(models.Model):
    date = models.DateField("Date")
    tournament = models.CharField("Tournament", max_length=240)
    matchId = models.CharField("MatchId", max_length=240)
    seriesId = models.IntegerField("SeriesId")
    patch = models.CharField("Patch", max_length=240)
    gameNumber = models.IntegerField("GameNumber")
    summonnerName = models.CharField("SummonnerName", max_length=240)
    xpd15 = models.IntegerField("XPD@15")
    gd15 = models.IntegerField("GD@15")
    kills = models.IntegerField("Kills")
    deaths = models.IntegerField("Deaths")
    assists = models.IntegerField("Assists")
    kp = models.FloatField("KP%")
    dpm = models.FloatField("Damage/Min")
    topLanePresence = models.FloatField("topLanePresence")
    midLanePresence = models.FloatField("midLanePresence")
    botLanePresence = models.FloatField("botLanePresence")
    jungleAllyTopPresence = models.FloatField("jungleAllyTopPresence")
    jungleAllyBotPresence = models.FloatField("jungleAllyBotPresence")
    jungleEnemyTopPresence = models.FloatField("jungleEnemyTopPresence")
    jungleEnemyBotPresence = models.FloatField("jungleEnemyBotPresence")
    riverBotPresence = models.FloatField("riverBotPresence")
    riverTopPresence = models.FloatField("riverTopPresence")

class BehaviorMid(models.Model):
    date = models.DateField("Date")
    tournament = models.CharField("Tournament", max_length=240)
    matchId = models.CharField("MatchId", max_length=240)
    seriesId = models.IntegerField("SeriesId")
    patch = models.CharField("Patch", max_length=240)
    gameNumber = models.IntegerField("GameNumber")
    summonnerName = models.CharField("SummonnerName", max_length=240)
    xpd15 = models.IntegerField("XPD@15")
    gd15 = models.IntegerField("GD@15")
    csMin = models.FloatField("CS/Min")
    kills = models.IntegerField("Kills")
    deaths = models.IntegerField("Deaths")
    assists = models.IntegerField("Assists")
    kp = models.FloatField("KP%")
    wardPlaced = models.IntegerField("WardPlaced")
    wardKilled = models.IntegerField("WardKilled")
    dpm = models.FloatField("Damage/Min")
    totalDamageDealtToBuilding = models.FloatField("TotalDamageDealtToBuilding")
    totalDamageDealtToObjectives = models.FloatField("TotalDamageDealtToObjectives")
    jungleProximity = models.FloatField("JungleProximity")
    topLanePresence = models.FloatField("topLanePresence")
    midLanePresence = models.FloatField("midLanePresence")
    botLanePresence = models.FloatField("botLanePresence")
    jungleAllyTopPresence = models.FloatField("jungleAllyTopPresence")
    jungleAllyBotPresence = models.FloatField("jungleAllyBotPresence")
    jungleEnemyTopPresence = models.FloatField("jungleEnemyTopPresence")
    jungleEnemyBotPresence = models.FloatField("jungleEnemyBotPresence")
    riverBotPresence = models.FloatField("riverBotPresence")
    riverTopPresence = models.FloatField("riverTopPresence")

class BehaviorADC(models.Model):
    date = models.DateField("Date")
    tournament = models.CharField("Tournament", max_length=240)
    matchId = models.CharField("MatchId", max_length=240)
    seriesId = models.IntegerField("SeriesId")
    patch = models.CharField("Patch", max_length=240)
    gameNumber = models.IntegerField("GameNumber")
    summonnerName = models.CharField("SummonnerName", max_length=240)
    xpd15 = models.IntegerField("XPD@15")
    gd15 = models.IntegerField("GD@15")
    csMin = models.FloatField("CS/Min")
    kills = models.IntegerField("Kills")
    deaths = models.IntegerField("Deaths")
    assists = models.IntegerField("Assists")
    kp = models.FloatField("KP%")
    dpm = models.FloatField("Damage/Min")
    jungleProximity = models.FloatField("JungleProximity")
    botLanePresence = models.FloatField("botLanePresence")
    riverBotPresence = models.FloatField("riverBotPresence")

class BehaviorSupport(models.Model):
    date = models.DateField("Date")
    tournament = models.CharField("Tournament", max_length=240)
    matchId = models.CharField("MatchId", max_length=240)
    seriesId = models.IntegerField("SeriesId")
    patch = models.CharField("Patch", max_length=240)
    gameNumber = models.IntegerField("GameNumber")
    summonnerName = models.CharField("SummonnerName", max_length=240)
    xpd15 = models.IntegerField("XPD@15")
    gd15 = models.IntegerField("GD@15")
    deaths = models.IntegerField("Deaths")
    kp = models.FloatField("KP%")
    wardPlaced = models.IntegerField("WardPlaced")
    wardKilled = models.IntegerField("WardKilled")
    dpm = models.FloatField("Damage/Min")
    jungleProximity = models.FloatField("JungleProximity")
    topLanePresence = models.FloatField("topLanePresence")
    midLanePresence = models.FloatField("midLanePresence")
    botLanePresence = models.FloatField("botLanePresence")
    jungleAllyTopPresence = models.FloatField("jungleAllyTopPresence")
    jungleAllyBotPresence = models.FloatField("jungleAllyBotPresence")
    jungleEnemyTopPresence = models.FloatField("jungleEnemyTopPresence")
    jungleEnemyBotPresence = models.FloatField("jungleEnemyBotPresence")
    riverBotPresence = models.FloatField("riverBotPresence")
    riverTopPresence = models.FloatField("riverTopPresence")