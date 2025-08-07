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


from django.utils.html import format_html

@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'service', 'status_dropdown', 'estimated_total', 'final_quote', 'created_at']
    list_filter = ['status', 'service', 'created_at']
    list_editable = ['final_quote']
    readonly_fields = ['selected_options', 'estimated_total', 'created_at']
    actions = ['mark_as_quoted', 'mark_as_accepted', 'mark_as_declined']
    
    def status_dropdown(self, obj):
        return format_html(
            '<select onchange="updateQuoteStatus({}, this.value)" class="form-control">' +
            '<option value="pending"{}>Pending</option>' +
            '<option value="in_review"{}>In Review</option>' +
            '<option value="quoted"{}>Quoted</option>' +
            '<option value="accepted"{}>Accepted</option>' +
            '<option value="declined"{}>Declined</option>' +
            '</select>',
            obj.id,
            ' selected' if obj.status == 'pending' else '',
            ' selected' if obj.status == 'in_review' else '',
            ' selected' if obj.status == 'quoted' else '',
            ' selected' if obj.status == 'accepted' else '',
            ' selected' if obj.status == 'declined' else ''
        )
    status_dropdown.short_description = 'Status'
    status_dropdown.allow_tags = True
    
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
    
    def changelist_view(self, request, extra_context=None):
        from core.models import AdminNotification
        extra_context = extra_context or {}
        extra_context['unread_notifications'] = AdminNotification.objects.filter(is_read=False, type='quote').count()
        return super().changelist_view(request, extra_context=extra_context)