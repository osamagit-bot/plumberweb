from django.contrib import admin
from .models import ServiceArea, Review, TrustBadge

@admin.register(ServiceArea)
class ServiceAreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'phone', 'is_active', 'created_at']
    list_filter = ['is_active', 'city', 'created_at']
    search_fields = ['name', 'phone', 'email', 'city']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'platform', 'rating', 'service_area', 'is_featured', 'date']
    list_filter = ['platform', 'rating', 'is_featured', 'service_area', 'date']
    search_fields = ['customer_name', 'review_text']

@admin.register(TrustBadge)
class TrustBadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'is_active']
    list_filter = ['is_active']