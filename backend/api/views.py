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
        lead_data = request.data
        
        # Calculate loan details
        principal = float(lead_data['loan_amount'])
        years = int(lead_data['loan_term'])
        rate = float(lead_data['interest_rate']) / 100 / 12
        number_of_payments = years * 12

        monthly_payment = (
            (principal * rate * (1 + rate) ** number_of_payments) /
            ((1 + rate) ** number_of_payments - 1)
        )
        total_payment = monthly_payment * number_of_payments
        total_interest = total_payment - principal

        # Create the lead instance
        lead = Lead(
            name=lead_data['name'],
            email=lead_data['email'],
            phone=lead_data['phone'],
            loan_amount=lead_data['loan_amount'],
            loan_term=lead_data['loan_term'],
            interest_rate=lead_data['interest_rate'],
            monthly_income=lead_data['monthly_income'],
            monthly_payment=round(monthly_payment, 2),  # Store calculated values
            total_payment=round(total_payment, 2),
            total_interest=round(total_interest, 2),
        )
        lead.save()

        # Send email after creating the lead
        send_report_email(lead)

        return JsonResponse({'status': 'success', 'message': 'Lead created successfully'})

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

def send_report_email(lead):
    subject = 'Your Loan Report Request'
    message = f"""
    Hello {lead.name},

    Thank you for your loan report request. Here are the details you submitted:

    Name: {lead.name}
    Email: {lead.email}
    Phone: {lead.phone}
    Loan Amount: {lead.loan_amount}
    Loan Term: {lead.loan_term}
    Interest Rate: {lead.interest_rate}
    Monthly Income: {lead.monthly_income}
    Monthly Payment: {lead.monthly_payment}
    Total Payment: {lead.total_payment}
    Total Interest: {lead.total_interest}
    
    We will get back to you shortly!

    Best regards,
    Sugar Rimz
    """
    recipient_list = [lead.email]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
