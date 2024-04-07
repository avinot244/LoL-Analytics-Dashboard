from rest_framework import serializers
from .models import DraftPickOrder, DraftPlayerPick

class DraftPickOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftPickOrder
        fields = ("pk", "date", "patch", "seriesId", "winner", "bb1", "bb2", "bb3", "bb4", "bb5", "bp1", "bp2", "bp3", "bp4", "bp5", "rb1", "rb2", "rb3", "rb4", "rb5", "rp1", "rp2", "rp3", "rp4", "rp5", "gameNumner")

class DraftPlayerPickSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftPlayerPick
        fields = ("pk", "date", "patch", "seriesId", "sumonnerName", "champioName", "role", "gameNumber")