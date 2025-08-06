from django.contrib import admin
from .models import Booking, ContactMessage

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'service', 'service_area', 'urgency', 'preferred_date', 'status', 'is_confirmed', 'created_at']
    list_filter = ['urgency', 'status', 'is_confirmed', 'created_at', 'service', 'service_area']
    search_fields = ['customer_name', 'email', 'phone']
    readonly_fields = ['created_at']
    list_editable = ['status', 'is_confirmed']
    actions = ['confirm_bookings', 'unconfirm_bookings', 'mark_completed']
    
    def confirm_bookings(self, request, queryset):
        updated = queryset.update(is_confirmed=True)
        self.message_user(request, f'{updated} booking(s) confirmed successfully.')
    confirm_bookings.short_description = "Confirm selected bookings"
    
    def unconfirm_bookings(self, request, queryset):
        updated = queryset.update(is_confirmed=False)
        self.message_user(request, f'{updated} booking(s) unconfirmed successfully.')
    unconfirm_bookings.short_description = "Unconfirm selected bookings"
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} booking(s) marked as completed.')
    mark_completed.short_description = "Mark selected bookings as completed"

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'service_area', 'email', 'created_at']
    list_filter = ['created_at', 'service_area']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']