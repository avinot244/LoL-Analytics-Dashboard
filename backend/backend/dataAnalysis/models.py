from django.db import models


class GameMetadata(models.Model):
    date = models.DateField("Date")
    tournament = models.CharField("Tournament", max_length=240)
    name = models.CharField("Name", max_length=240)
    patch = models.CharField("Patch", max_length=240)
    seriesId = models.IntegerField("Seriesid")
    teamBlue = models.CharField("teamBlue", max_length=240)
    teamRed = models.CharField("teamRed", max_length=240)
    winningTeam = models.IntegerField("winningTeam")
    gameNumber = models.IntegerField("gameNumber")
    dragonBlueKills = models.IntegerField("dragonBlueKills")
    dragonRedKills = models.IntegerField("dragonRedKills")
    voidGrubsBlueKills = models.IntegerField("voidGrubsBlueKills")
    voidGrubsRedKills = models.IntegerField("voidGrubsRedKills")
    heraldBlueKills = models.IntegerField("heraldBlueKills")
    heraldRedKills = models.IntegerField("heraldRedKills")
    baronBlueKills = models.IntegerField("baronBlueKills")
    baronRedKills = models.IntegerField("baronRedKills")
    elderBlueKills = models.IntegerField("elderBlueKills")
    elderRedKills = models.IntegerField("elderRedKills")
    firstBlood = models.IntegerField("firstBlood")
    firstTower = models.IntegerField("firstTower")
    turretBlueKills = models.IntegerField("turretBlueKills")
    turretRedKills = models.IntegerField("turretRedKills")
    