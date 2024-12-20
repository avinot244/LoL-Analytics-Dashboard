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
    krubsBlueKills = models.IntegerField("krubsBlueKills")
    krubsRedKills = models.IntegerField("krubsRedKills")