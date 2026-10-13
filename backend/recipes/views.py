from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ai.image_service import generate_recipe_image
from .models import Recipe
from .serializers import IngredientMatchSerializer, RecipeGenerationSerializer, RecipeSerializer
from .services import generate_all, match_ingredients

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    @action(detail=False, methods=["post"])
    def generate(self, request):
        serializer = RecipeGenerationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        result = generate_all(serializer.validated_data["ingredients"], serializer.validated_data["platform"], serializer.validated_data["servings"], serializer.validated_data["difficulty"])
        return Response(result, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def generate_all(self, request):
        serializer = RecipeGenerationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        result = generate_all(serializer.validated_data["ingredients"], serializer.validated_data["platform"], serializer.validated_data["servings"], serializer.validated_data["difficulty"])
        return Response(result, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def generate_image(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        image = generate_recipe_image({
            "name": recipe.name,
            "description": recipe.description,
            "ingredients": recipe.ingredients,
            "additional_ingredients": recipe.additional_ingredients,
            "servings": recipe.servings,
            "prep_time": recipe.preparation_time,
            "cook_time": recipe.cooking_time,
            "difficulty": recipe.difficulty,
            "instructions": recipe.instructions,
        }, recipe.ingredients)

        recipe.image_url = image.get("url") or ""
        recipe.image_status = image.get("status", "unavailable")
        recipe.image_error = image.get("error", "")
        recipe.save(update_fields=["image_url", "image_status", "image_error"])

        return Response({"image": image, "recipe_id": recipe.pk}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def match(self, request):
        serializer = IngredientMatchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(match_ingredients(serializer.validated_data["available"], serializer.validated_data["required"]))
