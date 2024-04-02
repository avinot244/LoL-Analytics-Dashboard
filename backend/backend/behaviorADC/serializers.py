from rest_framework import serializers
from .models import BehaviorADC, BehaviorTop

class BehaviorADCSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehaviorADC
        fields = ("pk", "date", "tournament", "matchId", "seriesId", "patch", "summonnerName", "xpd15", "gd15", "csMin", "kills", "deaths", "assists", "kp", "dpm", "jungleProximity", "botLanePresence", "riverBotPresence")

    
class BehaviorTopSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehaviorTop
        fields = ("pk", "Date", "Tournament", "MatchId", "SeriesId", "Patch", "SummonnerName", "XPD@15", "GD@15", "CS/Min", "Kills", "Deaths", "Assists", "KP%", "WardPlaced", "Damage/Min", "TotalDamageDealtToBuilding", "TotalDamageDealtToObjectives", "JungleProximity", "topLanePresence", "jungleAllyTopPresence", "jungleEnemyTopPresence", "riverTopPresence")