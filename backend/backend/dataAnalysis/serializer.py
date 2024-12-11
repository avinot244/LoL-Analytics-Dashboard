from rest_framework import serializers
from .models import GameMetadata

class GameMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameMetadata
        fields = (
            "pk",
            "date",
            "name",
            "patch",
            "seriesId",
            "teamBlue",
            "teamRed",
            "winningTeam",
            "gameNumber",
            "dragonBlueKills",
            "dragonRedKills",
            "krubsBlueKills",
            "krubsRedKills"
        )