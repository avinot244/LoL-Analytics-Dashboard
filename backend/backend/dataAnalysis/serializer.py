from rest_framework import serializers
from .models import GameMetadata

class GameMetadataSerialize(serializers.ModelSerializer):
    class Meta:
        model = GameMetadata
        fields = ("date", "name", "patch", "seriesId", "teamBlue", "teamRed", "winningTeam")