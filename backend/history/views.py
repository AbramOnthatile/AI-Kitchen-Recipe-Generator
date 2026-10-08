from rest_framework import status, viewsets
from rest_framework.response import Response
from .models import GenerationHistory
from .serializers import GenerationHistorySerializer, HistoryCreateSerializer

class HistoryViewSet(viewsets.ModelViewSet):
    queryset = GenerationHistory.objects.all()
    serializer_class = GenerationHistorySerializer

    def create(self, request):
        serializer = HistoryCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        history = GenerationHistory.objects.create(**serializer.validated_data)
        return Response(GenerationHistorySerializer(history).data, status=status.HTTP_201_CREATED)
