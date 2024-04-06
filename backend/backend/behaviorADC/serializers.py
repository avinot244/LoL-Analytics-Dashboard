from rest_framework import serializers
from .models import BehaviorADC, BehaviorTop

class BehaviorADCSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehaviorADC
        fields = ("pk", "date", "tournament", "matchId", "seriesId", "patch", "summonnerName", "xpd15", "gd15", "csMin", "kills", "deaths", "assists", "kp", "dpm", "jungleProximity", "botLanePresence", "riverBotPresence")

    
class BehaviorTopSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehaviorTop
        fields = ("pk", "date", "tournament", "matchId", "seriesId", "patch", "summonnerName", "xpd15", "gd15", "csMin", "kills", "deaths", "assists", "kp", "wardPlaced", "dpm", "totalDamageDealtToBuilding", "totalDamageDealtToObjectives", "jungleProximity", "topLanePresence", "jungleAllyTopPresence", "jungleEnemyTopPresence", "riverTopPresence")