from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    loan_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[
            MinValueValidator(Decimal('1000.00')),
            MaxValueValidator(Decimal('10000000.00'))
        ]
    )
    loan_term = models.IntegerField(default=12)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('5.99'))
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    monthly_payment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_payment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_interest = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name