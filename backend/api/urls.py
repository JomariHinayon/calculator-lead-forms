from django.urls import path
from .views import LeadListCreate, LeadDetail

urlpatterns = [
    path('leads/', LeadListCreate.as_view(), name='lead-list-create'),  # Keep this one for REST framework
    path('leads/<int:pk>/', LeadDetail.as_view(), name='lead-detail'),  # For retrieving, updating, and deleting a specific lead
]