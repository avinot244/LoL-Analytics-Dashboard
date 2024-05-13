from rest_framework import serializers
from .models import BehaviorTop, BehaviorJungle, BehaviorMid, BehaviorADC, BehaviorSupport

    
class BehaviorTopSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehaviorTop
        fields = ("pk", "date", "tournament", "matchId", "seriesId", "patch", "gameNumber", "summonnerName", "xpd15", "gd15", "csMin", "kills", "deaths", "assists", "kp", "wardPlaced", "dpm", "totalDamageDealtToBuilding", "totalDamageDealtToObjectives", "jungleProximity", "topLanePresence", "jungleAllyTopPresence", "jungleEnemyTopPresence", "riverTopPresence")

class BehaviorJungleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehaviorJungle
        fields = ("pk", "date", "tournament", "matchId", "seriesId", "patch", "gameNumber", "summonnerName", "xpd15", "gd15", "kills", "deaths", "assists", "kp" ,"dpm", "topLanePresence", "midLanePresence", "botLanePresence", "jungleAllyTopPresence", "jungleAllyBotPresence", "jungleEnemyTopPresence", "jungleEnemyBotPresence", "riverBotPresence", "riverTopPresence")

class BehaviorMidSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehaviorMid
        fields = ("pk", "date", "tournament", "matchId", "seriesId", "patch", "gameNumber", "summonnerName", "xpd15", "gd15", "csMin", "kills", "deaths", "assists", "kp", "wardPlaced" , "wardKilled", "dpm", "totalDamageDealtToBuilding", "totalDamageDealtToObjectives", "jungleProximity", "topLanePresence", "midLanePresence", "botLanePresence", "jungleAllyTopPresence", "jungleAllyBotPresence", "jungleEnemyTopPresence", "jungleEnemyBotPresence", "riverBotPresence", "riverTopPresence")

class BehaviorADCSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehaviorADC
        fields = ("pk", "date", "tournament", "matchId", "seriesId", "patch", "gameNumber", "summonnerName", "xpd15", "gd15", "csMin", "kills", "deaths", "assists", "kp", "dpm", "jungleProximity", "botLanePresence", "riverBotPresence")


class BehaviorSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehaviorSupport
        fields = ("pk", "date", "tournament", "matchId", "seriesId", "patch", "gameNumber", "summonnerName", "xpd15", "gd15", "deaths", "kp", "wardPlaced", "wardKilled", "dpm", "jungleProximity", "topLanePresence", "midLanePresence", "botLanePresence", "jungleAllyTopPresence", "jungleAllyBotPresence", "jungleEnemyTopPresence", "jungleEnemyBotPresence", "riverBotPresence", "riverTopPresence")