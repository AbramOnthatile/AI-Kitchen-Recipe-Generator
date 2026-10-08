from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet

router = DefaultRouter()
router.register("recipes", RecipeViewSet, basename="recipe")
urlpatterns = [
    path("recipes/generate-all/", RecipeViewSet.as_view({"post": "generate_all"}), name="recipe-generate-all"),
    path("recipes/generate/", RecipeViewSet.as_view({"post": "generate"}), name="recipe-generate"),
    *router.urls,
]
