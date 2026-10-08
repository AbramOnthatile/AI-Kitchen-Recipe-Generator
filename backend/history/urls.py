from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import HistoryViewSet

router = DefaultRouter()
router.register("history", HistoryViewSet, basename="history")
urlpatterns = router.urls
