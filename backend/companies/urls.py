from django.urls import path
from .views import CompanyViewSet, CompanyStageViewSet

company_list = CompanyViewSet.as_view({'get': 'list', 'post': 'create'})
company_detail = CompanyViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})
stage_list = CompanyStageViewSet.as_view({'get': 'list', 'post': 'create'})
stage_detail = CompanyStageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})

urlpatterns = [
    path('companies/', company_list),
    path('companies/<int:pk>/', company_detail),
    path('companies/<int:company_pk>/stages/', stage_list),
    path('companies/<int:company_pk>/stages/<int:pk>/', stage_detail),
]
