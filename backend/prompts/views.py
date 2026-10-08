from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ai.services import analyse_prompt, optimize_prompt
from .models import Prompt, PromptVersion
from .serializers import PromptAnalyzeSerializer, PromptCreateSerializer, PromptOptimizeSerializer, PromptSerializer, PromptVersionSerializer

class PromptViewSet(viewsets.ModelViewSet):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    def get_serializer_class(self):
        return PromptCreateSerializer if self.action == "create" else PromptSerializer

    @action(detail=False, methods=["post"])
    def optimize(self, request):
        serializer = PromptOptimizeSerializer(data=request.data)
        if not serializer.is_valid(): return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        result = optimize_prompt(serializer.validated_data["prompt"], serializer.validated_data["goal"])
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def analyse(self, request):
        serializer = PromptAnalyzeSerializer(data=request.data)
        if not serializer.is_valid(): return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(analyse_prompt(serializer.validated_data["prompt"]), status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def versions(self, request, pk=None):
        prompt = self.get_object()
        version = PromptVersion.objects.create(prompt=prompt, version_number=prompt.versions.count() + 1, prompt_text=request.data.get("prompt_text", prompt.prompt_text), score=request.data.get("score", 0))
        return Response(PromptVersionSerializer(version).data, status=status.HTTP_201_CREATED)
