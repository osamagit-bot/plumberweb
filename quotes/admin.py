from django.contrib import admin
from .models import QuoteCalculator, QuoteOption, QuoteRequest


class QuoteOptionInline(admin.TabularInline):
    model = QuoteOption
    extra = 1


@admin.register(QuoteCalculator)
class QuoteCalculatorAdmin(admin.ModelAdmin):
    list_display = ['service', 'base_price', 'labor_rate_per_hour', 'is_active']
    list_filter = ['is_active']
    inlines = [QuoteOptionInline]


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'service', 'status', 'estimated_total', 'final_quote', 'created_at']
    list_filter = ['status', 'service', 'created_at']
    list_editable = ['status', 'final_quote']
    readonly_fields = ['selected_options', 'estimated_total', 'created_at']
    actions = ['mark_as_quoted', 'mark_as_accepted', 'mark_as_declined']
    
    def mark_as_quoted(self, request, queryset):
        updated = queryset.update(status='quoted')
        self.message_user(request, f'{updated} quote(s) marked as quoted.')
    mark_as_quoted.short_description = "Mark selected quotes as quoted"
    
    def mark_as_accepted(self, request, queryset):
        updated = queryset.update(status='accepted')
        self.message_user(request, f'{updated} quote(s) marked as accepted.')
    mark_as_accepted.short_description = "Mark selected quotes as accepted"
    
    def mark_as_declined(self, request, queryset):
        updated = queryset.update(status='declined')
        self.message_user(request, f'{updated} quote(s) marked as declined.')
    mark_as_declined.short_description = "Mark selected quotes as declined"