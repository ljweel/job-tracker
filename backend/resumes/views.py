from rest_framework import viewsets, parsers
from .models import ResumeEvent
from .serializers import ResumeEventSerializer


class ResumeEventViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeEventSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    def get_queryset(self):
        return ResumeEvent.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
