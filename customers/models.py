from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    service_area = models.ForeignKey(
        'areas.ServiceArea',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customers',
        help_text="Customer's service location"
    )
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)
    emergency_phone = models.CharField(max_length=20, blank=True, null=True)
    preferred_contact_method = models.CharField(
        max_length=20,
        choices=[
            ('email', 'Email'),
            ('phone', 'Phone'),
            ('text', 'Text Message'),
        ],
        default='email'
    )
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.user.email}"

    def get_absolute_url(self):
        return reverse('customers:profile')

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip()

    @property
    def full_address(self):
        parts = [self.address, self.city, self.postal_code]
        return ", ".join([part for part in parts if part])


class CustomerNote(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='notes')
    note = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_internal = models.BooleanField(default=True)  # Only visible to staff

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Note for {self.customer.full_name} - {self.created_at.strftime('%Y-%m-%d')}"


class CustomerDocument(models.Model):
    DOCUMENT_TYPES = [
        ('invoice', 'Invoice'),
        ('quote', 'Quote'),
        ('warranty', 'Warranty'),
        ('receipt', 'Receipt'),
        ('report', 'Service Report'),
        ('other', 'Other'),
    ]

    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, default='other')
    file = models.FileField(upload_to='customer_documents/')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)  # Visible to customer

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.customer.full_name}"
