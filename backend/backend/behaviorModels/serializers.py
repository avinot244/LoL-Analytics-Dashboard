from rest_framework import serializers
from .models import BehaviorModelsMetadata

class BehaviorModelsMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehaviorModelsMetadata
        fields = ("pk", "uuid", "modelType", "modelName", "role", "kmo", "tournamentDict")


