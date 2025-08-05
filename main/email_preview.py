"""
Email preview views for testing email templates
Only for development/testing purposes
"""
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from services.models import Service
from areas.models import ServiceArea
from bookings.models import Booking, ContactMessage
from datetime import date, datetime
from django.utils import timezone

def preview_booking_email(request):
    """Preview booking confirmation email"""
    try:
        # Create sample booking data
        service = Service.objects.first()
        service_area = ServiceArea.objects.first()
        
        # Create a fake booking for preview
        sample_booking = Booking(
            customer_name="John Smith",
            email="john.smith@example.com",
            phone="+1-647-555-0123",
            address="123 Main Street, Toronto, ON M5V 1A1",
            service=service,
            service_area=service_area,
            urgency="high",
            preferred_date=date.today(),
            description="Kitchen sink is completely blocked and overflowing. Water everywhere!"
        )
        
        # Render the email template
        html_content = render_to_string('emails/booking_confirmation.html', {
            'booking': sample_booking
        })
        
        return HttpResponse(html_content)
        
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

def preview_admin_email(request):
    """Preview admin booking notification email"""
    try:
        # Create sample booking data
        service = Service.objects.filter(is_emergency=True).first()
        service_area = ServiceArea.objects.first()
        
        # Create a fake emergency booking for preview
        sample_booking = Booking(
            customer_name="Jane Doe",
            email="jane.doe@example.com", 
            phone="+1-647-555-0199",
            address="456 Emergency Lane, Toronto, ON M5V 2B2",
            service=service,
            service_area=service_area,
            urgency="emergency",
            preferred_date=date.today(),
            description="EMERGENCY: Basement flooding from burst pipe!"
        )
        
        # Render the admin email template
        html_content = render_to_string('emails/admin_booking_notification.html', {
            'booking': sample_booking
        })
        
        return HttpResponse(html_content)
        
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

def preview_contact_email(request):
    """Preview contact confirmation email"""
    try:
        service_area = ServiceArea.objects.first()
        
        # Create a fake contact message for preview
        sample_contact = ContactMessage(
            name="Mike Johnson",
            email="mike.johnson@example.com",
            phone="+1-647-555-0177",
            subject="Question about water heater installation",
            message="Hi, I'm interested in replacing my old water heater. Can you provide a quote for a new tankless unit? My current heater is about 15 years old.",
            service_area=service_area
        )
        
        # Render the contact email template
        html_content = render_to_string('emails/contact_confirmation.html', {
            'contact': sample_contact
        })
        
        return HttpResponse(html_content)
        
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
