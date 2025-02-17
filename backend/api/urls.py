from django.urls import path
from .views import LeadListCreate

urlpatterns = [
    path('leads/', LeadListCreate.as_view(), name='lead-list-create'),
]