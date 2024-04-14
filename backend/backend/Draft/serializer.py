from rest_framework import serializers
from .models import DraftPickOrder, DraftPlayerPick, ChampionDraftStats

class DraftPickOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftPickOrder
        fields = ("pk", "date", "patch", "seriesId", "teamBlue", "teamRed", "winner", "bb1", "bb2", "bb3", "bb4", "bb5", "bp1", "bp2", "bp3", "bp4", "bp5", "rb1", "rb2", "rb3", "rb4", "rb5", "rp1", "rp2", "rp3", "rp4", "rp5", "gameNumner")

class DraftPlayerPickSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftPlayerPick
        fields = ("pk", "date", "patch", "seriesId", "sumonnerName", "champioName", "role", "gameNumber")

class ChampionDraftStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChampionDraftStats
        fields = ("pk", "championName", "patch", "tournament", "side", "mostPopularRole", "winRate", "globalPickRate", "pickRate1Rota", "pickRate2Rota", "globalBanRate", "banRate1Rota", "banRate2Rota", "mostPopularPickOrder", "blindPick", "mostPopularRole")