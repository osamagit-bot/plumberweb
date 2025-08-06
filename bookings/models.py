from django.db import models
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
from services.models import Service
from areas.models import ServiceArea
from core.constants import URGENCY_CHOICES


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    # Link to customer account (optional for backwards compatibility)
    customer = models.ForeignKey(
        'customers.CustomerProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bookings'
    )
    
    # Original fields (kept for backwards compatibility)
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = PhoneNumberField(region='CA')
    address = models.TextField()
    service = models.ForeignKey(
        Service, 
        on_delete=models.PROTECT,  # Don't delete bookings if service is deleted
        related_name='bookings'
    )
    service_area = models.ForeignKey(
        ServiceArea, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='bookings'
    )
    urgency = models.CharField(
        max_length=20, 
        choices=URGENCY_CHOICES,
        db_index=True
    )
    preferred_date = models.DateTimeField()
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )
    is_confirmed = models.BooleanField(default=False, db_index=True)
    notes = models.TextField(blank=True, help_text="Internal notes")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return f"{self.customer_name} - {self.service.name} ({self.get_urgency_display()})"

    @property
    def is_emergency(self):
        return self.urgency == 'emergency'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('booking_detail', kwargs={'pk': self.pk})


class ContactMessage(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = PhoneNumberField(region='CA', blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    service_area = models.ForeignKey(
        ServiceArea, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='contact_messages'
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        db_index=True
    )
    is_read = models.BooleanField(default=False, db_index=True)
    is_resolved = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} - {self.subject}"

    def mark_as_read(self):
        self.is_read = True
        self.save(update_fields=['is_read', 'updated_at'])

    def mark_as_resolved(self):
        self.is_resolved = True
        self.save(update_fields=['is_resolved', 'updated_at'])