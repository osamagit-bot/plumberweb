from django.urls import path
from . import admin_views

app_name = 'core'

urlpatterns = [
    # API Endpoints for status updates
    path('admin/api/bookings/<int:booking_id>/', admin_views.booking_status_api, name='booking_status_api'),
    path('admin/api/quotes/<int:quote_id>/', admin_views.quote_status_api, name='quote_status_api'),
]