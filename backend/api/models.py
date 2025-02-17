from django.db import models

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    loan_term = models.IntegerField(default=12)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.99)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name