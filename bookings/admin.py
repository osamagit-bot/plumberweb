from django.contrib import admin
from .models import Booking, ContactMessage

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'service', 'service_area', 'urgency', 'preferred_date', 'is_confirmed', 'created_at']
    list_filter = ['urgency', 'is_confirmed', 'created_at', 'service', 'service_area']
    search_fields = ['customer_name', 'email', 'phone']
    readonly_fields = ['created_at']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'service_area', 'email', 'created_at']
    list_filter = ['created_at', 'service_area']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']