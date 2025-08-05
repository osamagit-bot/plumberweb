from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryImage


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'service', 'location', 'is_featured', 'is_active', 'order', 'image_preview', 'has_before_after']
    list_filter = ['category', 'service', 'location', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_featured', 'is_active', 'order']
    readonly_fields = ['image_preview', 'before_image_preview', 'after_image_preview', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'image', 'image_preview')
        }),
        ('Before & After Images', {
            'fields': ('before_image', 'before_image_preview', 'after_image', 'after_image_preview'),
            'description': 'Upload before and after images for comparison galleries. These are optional and mainly used for before_after category.'
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
    
    def before_image_preview(self, obj):
        if obj.before_image:
            return format_html(
                '<img src="{}" style="max-width: 150px; max-height: 150px; object-fit: cover;" />',
                obj.before_image.url
            )
        return "No before image"
    before_image_preview.short_description = "Before Preview"
    
    def after_image_preview(self, obj):
        if obj.after_image:
            return format_html(
                '<img src="{}" style="max-width: 150px; max-height: 150px; object-fit: cover;" />',
                obj.after_image.url
            )
        return "No after image"
    after_image_preview.short_description = "After Preview"
    
    def has_before_after(self, obj):
        return bool(obj.before_image and obj.after_image)
    has_before_after.short_description = "Before/After"
    has_before_after.boolean = True
