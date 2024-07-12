from django.urls import path
from .views import workflow_home, list_requests, request_detail, approve_request, reject_request

app_name = 'workflow'

urlpatterns = [
    path('', workflow_home, name='workflow_home'),
    path('requests/', list_requests, name='list_requests'),
    path('requests/<int:pk>/', request_detail, name='request_detail'),
    path('requests/<int:pk>/approve/', approve_request, name='approve_request'),
    path('requests/<int:pk>/reject/', reject_request, name='reject_request'),
]
