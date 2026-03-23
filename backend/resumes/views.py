from rest_framework import viewsets, parsers
from .models import ResumeEvent
from .serializers import ResumeEventSerializer


class ResumeEventViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeEventSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    queryset = ResumeEvent.objects.all()
