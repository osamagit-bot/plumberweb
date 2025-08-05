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
    list_display = ['customer_name', 'service', 'estimated_total', 'created_at']
    list_filter = ['service', 'created_at']
    readonly_fields = ['selected_options', 'estimated_total', 'created_at']