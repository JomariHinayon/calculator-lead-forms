from rest_framework import generics
from .models import Lead
from .serializers import LeadSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

class LeadListCreate(generics.ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

class LeadDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

@csrf_exempt  # Use this for testing; consider using CSRF protection in production
def create_lead(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            lead = Lead(
                name=data.get('name'),
                email=data.get('email'),
                phone=data.get('phone'),
                loan_amount=data.get('loan_amount'),
                loan_term=data.get('loan_term'),
                interest_rate=data.get('interest_rate'),
                monthly_income=data.get('monthly_income'),
                message=data.get('message', ''),
            )
            lead.save()
            return JsonResponse({'status': 'success', 'message': 'Lead created successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)