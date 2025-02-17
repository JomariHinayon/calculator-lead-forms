from django.urls import path
from .views import LeadListCreate, LeadDetail, create_lead

urlpatterns = [
    path('leads/', LeadListCreate.as_view(), name='lead-list-create'),  # For listing and creating leads
    path('leads/<int:pk>/', LeadDetail.as_view(), name='lead-detail'),  # For retrieving, updating, and deleting a specific lead
    path('leads/', create_lead, name='create_lead'),  # Ensure this matches your frontend request
]