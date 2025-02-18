from rest_framework import generics
from .models import Lead
from .serializers import LeadSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import send_mail
from django.conf import settings

class LeadListCreate(generics.ListCreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    def create(self, request, *args, **kwargs):
        print("Received data:", request.data)  # Add this line for debugging
        response = super().create(request, *args, **kwargs)
        
        # Send email after creating the lead
        lead_data = request.data
        send_report_email(lead_data)
        
        return response

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

def send_report_email(lead_data):
    subject = 'Your Loan Report Request'
    message = f"""
    Hello {lead_data['name']},

    Thank you for your loan report request. Here are the details you submitted:

    Name: {lead_data['name']}
    Email: {lead_data['email']}
    Phone: {lead_data['phone']}
    Loan Amount: {lead_data['loan_amount']}
    Loan Term: {lead_data['loan_term']}
    Interest Rate: {lead_data['interest_rate']}
    Monthly Income: {lead_data['monthly_income']}
    
    We will get back to you shortly!

    Best regards,
    Sugar Rimz
    """
    recipient_list = [lead_data['email']]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
