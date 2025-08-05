from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryImage


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'service', 'location', 'is_featured', 'is_active', 'order', 'image_preview']
    list_filter = ['category', 'service', 'location', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_featured', 'is_active', 'order']
    readonly_fields = ['image_preview', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'image', 'image_preview')
        }),
        ('Categorization', {
            'fields': ('category', 'service', 'location')
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px; object-fit: cover;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Preview"
