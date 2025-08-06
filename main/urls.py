from django.urls import path
from . import views
from .email_preview import preview_booking_email, preview_admin_email, preview_contact_email

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services_view, name='services'),
    path('booking/', views.booking_view, name='booking'),
    path('contact/', views.contact_view, name='contact'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('feedback/', views.feedback_view, name='feedback'),
    
    # Email preview URLs (for testing only)
    path('preview/email/booking/', preview_booking_email, name='preview_booking_email'),
    path('preview/email/admin/', preview_admin_email, name='preview_admin_email'),
    path('preview/email/contact/', preview_contact_email, name='preview_contact_email'),
]