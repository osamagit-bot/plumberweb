from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from .models import CustomerProfile, CustomerNote, CustomerDocument


class CustomerProfileInline(admin.StackedInline):
    model = CustomerProfile
    can_delete = False
    verbose_name_plural = 'Customer Profile'


class CustomerUserAdmin(DefaultUserAdmin):
    inlines = (CustomerProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined')
    list_filter = ('is_active', 'date_joined', 'customerprofile__created_at')


class CustomerNoteInline(admin.TabularInline):
    model = CustomerNote
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('note', 'created_by', 'is_internal', 'created_at')


class CustomerDocumentInline(admin.TabularInline):
    model = CustomerDocument
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('title', 'document_type', 'file', 'is_public', 'created_at')


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'service_area', 'city', 'preferred_contact_method', 'created_at')
    list_filter = ('service_area', 'preferred_contact_method', 'email_notifications', 'sms_notifications', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone', 'service_area__name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CustomerNoteInline, CustomerDocumentInline]
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Location Information', {
            'fields': ('service_area',)
        }),
        ('Contact Information', {
            'fields': ('phone', 'address', 'city', 'postal_code')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact', 'emergency_phone')
        }),
        ('Preferences', {
            'fields': ('preferred_contact_method', 'email_notifications', 'sms_notifications')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(CustomerNote)
class CustomerNoteAdmin(admin.ModelAdmin):
    list_display = ('customer', 'note_preview', 'created_by', 'is_internal', 'created_at')
    list_filter = ('is_internal', 'created_at')
    search_fields = ('customer__user__username', 'customer__user__email', 'note')
    readonly_fields = ('created_at',)
    
    def note_preview(self, obj):
        return obj.note[:50] + '...' if len(obj.note) > 50 else obj.note
    note_preview.short_description = 'Note Preview'


@admin.register(CustomerDocument)
class CustomerDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer', 'document_type', 'is_public', 'created_at')
    list_filter = ('document_type', 'is_public', 'created_at')
    search_fields = ('title', 'customer__user__username', 'customer__user__email')
    readonly_fields = ('created_at',)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomerUserAdmin)
