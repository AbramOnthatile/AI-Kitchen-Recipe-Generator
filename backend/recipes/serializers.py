from rest_framework import serializers
from .models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"

class RecipeGenerationSerializer(serializers.Serializer):
    ingredients = serializers.ListField(child=serializers.CharField(max_length=80), min_length=1)
    platform = serializers.ChoiceField(choices=[("Instagram", "Instagram"), ("Facebook", "Facebook"), ("LinkedIn", "LinkedIn"), ("X", "X")], default="Instagram")
    servings = serializers.IntegerField(min_value=1, max_value=50, required=False, default=4)
    difficulty = serializers.ChoiceField(choices=[("Easy", "Easy"), ("Medium", "Medium"), ("Advanced", "Advanced")], required=False, default="Easy")

class IngredientMatchSerializer(serializers.Serializer):
    available = serializers.ListField(child=serializers.CharField(max_length=80), min_length=1)
    required = serializers.ListField(child=serializers.CharField(max_length=80), min_length=1)
