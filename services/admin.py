from django.contrib import admin
from .models import Service, Testimonial, FAQ

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_range', 'is_emergency', 'created_at']
    list_filter = ['is_emergency', 'created_at']
    search_fields = ['name', 'description']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'service', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'service']
    search_fields = ['customer_name', 'comment']

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_active']