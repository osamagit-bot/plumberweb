from django.contrib import admin
from django.utils.html import format_html
from .models import Booking, ContactMessage

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'service', 'service_area', 'urgency', 'preferred_date', 'status', 'is_confirmed', 'created_at']
    list_filter = ['urgency', 'status', 'is_confirmed', 'created_at', 'service', 'service_area']
    search_fields = ['customer_name', 'email', 'phone']
    readonly_fields = ['created_at']
    actions = ['confirm_bookings', 'unconfirm_bookings', 'mark_completed', 'mark_pending', 'mark_cancelled', 'mark_in_progress']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'email', 'phone')
        }),
        ('Service Details', {
            'fields': ('service', 'service_area', 'urgency', 'preferred_date', 'preferred_time')
        }),
        ('Booking Status', {
            'fields': ('status', 'is_confirmed')
        }),
        ('Additional Information', {
            'fields': ('description', 'created_at'),
            'classes': ('collapse',)
        })
    )
    

    
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
    
    def mark_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} booking(s) marked as pending.')
    mark_pending.short_description = "Mark selected bookings as pending"
    
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} booking(s) marked as cancelled.')
    mark_cancelled.short_description = "Mark selected bookings as cancelled"
    
    def mark_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} booking(s) marked as in progress.')
    mark_in_progress.short_description = "Mark selected bookings as in progress"
    
    def changelist_view(self, request, extra_context=None):
        from core.models import AdminNotification
        extra_context = extra_context or {}
        extra_context['unread_notifications'] = AdminNotification.objects.filter(is_read=False, type='booking').count()
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'service_area', 'email', 'created_at']
    list_filter = ['created_at', 'service_area']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Message Details', {
            'fields': ('subject', 'service_area', 'message')
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    

    
    def changelist_view(self, request, extra_context=None):
        from core.models import AdminNotification
        extra_context = extra_context or {}
        extra_context['unread_notifications'] = AdminNotification.objects.filter(is_read=False, type='contact').count()
        return super().changelist_view(request, extra_context=extra_context)