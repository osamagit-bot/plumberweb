from django.contrib import admin
from .models import Service, Testimonial, FAQ

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_range', 'is_emergency', 'created_at']
    list_filter = ['is_emergency', 'created_at']
    search_fields = ['name', 'description']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'service', 'location', 'rating_stars', 'is_approved', 'is_verified', 'created_at']
    list_filter = ['rating', 'is_approved', 'is_verified', 'created_at', 'service', 'location']
    search_fields = ['customer_name', 'email', 'comment', 'title']
    list_editable = ['is_approved', 'is_verified']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'email', 'phone')
        }),
        ('Review Details', {
            'fields': ('title', 'comment', 'rating', 'service', 'location')
        }),
        ('Verification & Approval', {
            'fields': ('is_approved', 'is_verified', 'google_review_url')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_reviews', 'verify_reviews', 'disapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} reviews were approved.')
    approve_reviews.short_description = "Approve selected reviews"
    
    def verify_reviews(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} reviews were marked as verified.')
    verify_reviews.short_description = "Mark selected reviews as verified"
    
    def disapprove_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} reviews were disapproved.')
    disapprove_reviews.short_description = "Disapprove selected reviews"
    
    def rating_stars(self, obj):
        """Display rating as stars in admin"""
        stars = '⭐' * obj.rating + '☆' * (5 - obj.rating)
        return f"{stars} ({obj.rating}/5)"
    rating_stars.short_description = "Rating"

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_active']