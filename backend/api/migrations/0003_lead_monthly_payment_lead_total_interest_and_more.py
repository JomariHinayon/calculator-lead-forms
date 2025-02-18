# Generated by Django 5.1.6 on 2025-02-18 20:26

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_lead_interest_rate_lead_loan_amount_lead_loan_term_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='monthly_payment',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='total_interest',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='total_payment',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='interest_rate',
            field=models.DecimalField(decimal_places=2, default=Decimal('5.99'), max_digits=5),
        ),
        migrations.AlterField(
            model_name='lead',
            name='loan_amount',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('1000.00')), django.core.validators.MaxValueValidator(Decimal('10000000.00'))]),
        ),
        migrations.AlterField(
            model_name='lead',
            name='monthly_income',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
