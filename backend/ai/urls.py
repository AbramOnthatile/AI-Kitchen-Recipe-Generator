from django.urls import path
from rest_framework.response import Response
from rest_framework.views import APIView

class HealthView(APIView):
    def get(self, request):
        return Response({"status": "ok", "service": "ai-kitchen-recipe-generator", "local_mode": not __import__("django.conf").conf.settings.AI_API_KEY})

urlpatterns = [path("health/", HealthView.as_view())]
