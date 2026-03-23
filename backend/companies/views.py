from rest_framework import viewsets
from rest_framework.exceptions import NotFound
from django.db.models import Min, Max
from .models import Company, CompanyStage
from .serializers import CompanyListSerializer, CompanyDetailSerializer, CompanyStageSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CompanyDetailSerializer
        return CompanyListSerializer

    def get_queryset(self):
        qs = Company.objects.all().annotate(first_stage_date=Min('stages__date'), last_stage_date=Max('stages__date'))
        if self.action == 'retrieve':
            qs = qs.prefetch_related('stages')
        return qs


class CompanyStageViewSet(viewsets.ModelViewSet):
    serializer_class = CompanyStageSerializer

    def get_queryset(self):
        return CompanyStage.objects.filter(
            company_id=self.kwargs['company_pk'],
        )

    def perform_create(self, serializer):
        try:
            company = Company.objects.get(pk=self.kwargs['company_pk'])
        except Company.DoesNotExist:
            raise NotFound('Company not found')
        serializer.save(company=company)
