from django.contrib import admin
from .models import Lead

class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'loan_amount', 'loan_term', 'interest_rate', 'monthly_income')
    search_fields = ('name', 'email', 'phone')

# Register your models here.
admin.site.register(Lead, LeadAdmin)
