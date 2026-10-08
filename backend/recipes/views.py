from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
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

    @action(detail=False, methods=["post"])
    def match(self, request):
        serializer = IngredientMatchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(match_ingredients(serializer.validated_data["available"], serializer.validated_data["required"]))
