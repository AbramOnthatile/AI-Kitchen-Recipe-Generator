from rest_framework import serializers
from .models import Prompt, PromptVersion

class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = "__all__"

class PromptCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ["id", "name", "category", "purpose", "prompt_text", "variables"]

class PromptVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptVersion
        fields = "__all__"

class PromptOptimizeSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=5000, min_length=3)
    goal = serializers.CharField(max_length=1000, required=False, default="")

class PromptAnalyzeSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=5000, min_length=3)
