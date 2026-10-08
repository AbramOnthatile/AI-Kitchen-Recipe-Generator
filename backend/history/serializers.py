from rest_framework import serializers
from .models import GenerationHistory

class GenerationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GenerationHistory
        fields = "__all__"

class HistoryCreateSerializer(serializers.Serializer):
    ingredients = serializers.ListField(child=serializers.CharField(max_length=80), min_length=1)
    recipe = serializers.DictField()
    cooking_instructions = serializers.ListField(child=serializers.CharField(max_length=500))
    social_media_post = serializers.DictField()
    platform = serializers.CharField(max_length=40, default="Instagram")
