from django.urls import path
from .views import ResumeEventViewSet

resume_list = ResumeEventViewSet.as_view({'get': 'list', 'post': 'create'})
resume_detail = ResumeEventViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})

urlpatterns = [
    path('resumes/', resume_list),
    path('resumes/<int:pk>/', resume_detail),
]
