from django.db import models
from services.models import Service


class QuoteCalculator(models.Model):
    service = models.OneToOneField(Service, on_delete=models.CASCADE, related_name='calculator')
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    labor_rate_per_hour = models.DecimalField(max_digits=6, decimal_places=2)
    estimated_hours = models.DecimalField(max_digits=4, decimal_places=1)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Calculator for {self.service.name}"


class QuoteOption(models.Model):
    calculator = models.ForeignKey(QuoteCalculator, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    price_modifier = models.DecimalField(max_digits=6, decimal_places=2, help_text="Additional cost")
    is_required = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.calculator.service.name} - {self.name}"


class QuoteRequest(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    selected_options = models.JSONField(default=list)
    estimated_total = models.DecimalField(max_digits=8, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Quote for {self.customer_name} - {self.service.name}"