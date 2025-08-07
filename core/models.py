from django.db import models
from django.contrib.auth.models import User

class AdminNotification(models.Model):
    NOTIFICATION_TYPES = [
        ('booking', 'New Booking'),
        ('contact', 'New Contact Message'),
        ('quote', 'New Quote Request'),
    ]
    
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_id = models.PositiveIntegerField(help_text="ID of the related booking/contact/quote")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.title}"