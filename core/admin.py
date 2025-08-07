from django.contrib import admin
from .models import AdminNotification

@admin.register(AdminNotification)
class AdminNotificationAdmin(admin.ModelAdmin):
    list_display = ['type', 'title', 'is_read', 'created_at']
    list_filter = ['type', 'is_read', 'created_at']
    list_editable = ['is_read']
    readonly_fields = ['created_at', 'related_id']
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} notification(s) marked as read.')
    mark_as_read.short_description = "Mark selected notifications as read"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} notification(s) marked as unread.')
    mark_as_unread.short_description = "Mark selected notifications as unread"
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')