from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from rest_framework.views import APIView


class RootView(APIView):
    def get(self, request):
        return JsonResponse(
            {
                "message": "AI Kitchen Recipe Generator API is running",
                "status": "ok",
            }
        )


urlpatterns = [
    path("", RootView.as_view(), name="root"),
    path("admin/", admin.site.urls),
    path("api/", include("recipes.urls")),
    path("api/", include("prompts.urls")),
    path("api/", include("history.urls")),
    path("api/", include("ai.urls")),
]
