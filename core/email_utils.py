"""
Email utility functions for SPRO Plumbing website
"""
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def send_booking_confirmation_email(booking):
    """
    Send booking confirmation email to customer
    """
    try:
        subject = f"Booking Confirmation - {booking.service.name} in {booking.service_area.name}"
        
        # Handle preferred_date formatting
        preferred_date_str = "Not specified"
        if booking.preferred_date:
            try:
                # Convert to local timezone if timezone-aware
                if hasattr(booking.preferred_date, 'astimezone'):
                    local_date = timezone.localtime(booking.preferred_date)
                else:
                    local_date = booking.preferred_date
                
                # Format as user-friendly string with date and time
                preferred_date_str = local_date.strftime('%B %d, %Y at %I:%M %p')
            except Exception as e:
                logger.warning(f"Error formatting preferred_date: {e}")
                preferred_date_str = str(booking.preferred_date)
        
        # Render HTML email
        html_content = render_to_string('emails/booking_confirmation.html', {
            'booking': booking,
            'preferred_date_formatted': preferred_date_str
        })
        
        # Create text version (fallback)
        text_content = f"""
        Dear {booking.customer_name},
        
        Thank you for choosing SPRO Plumbing! We've received your service request for {booking.service.name} in {booking.service_area.name}.
        
        Booking Details:
        - Service: {booking.service.name}
        - Location: {booking.service_area.name}
        - Preferred Date: {preferred_date_str}
        - Urgency: {booking.get_urgency_display()}
        - Address: {booking.address}
        
        Our team will contact you at {booking.phone} within 2 hours to confirm the appointment.
        
        For emergencies, call: (647) 551-8342
        
        Best regards,
        SPRO Plumbing Team
        """
        
        # Send email
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[booking.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        logger.info(f"Booking confirmation email sent to {booking.email} for booking #{booking.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send booking confirmation email: {str(e)}")
        return False

def send_contact_confirmation_email(contact):
    """
    Send contact form confirmation email to customer
    """
    try:
        subject = f"Message Received - {contact.subject}"
        
        # Render HTML email
        html_content = render_to_string('emails/contact_confirmation.html', {
            'contact': contact
        })
        
        # Create text version (fallback)
        text_content = f"""
        Dear {contact.name},
        
        Thank you for contacting SPRO Plumbing! We've received your message about "{contact.subject}" and will get back to you within 24 hours.
        
        Your Message:
        {contact.message}
        
        For urgent emergencies, call: (647) 551-8342
        
        Best regards,
        SPRO Plumbing Team
        """
        
        # Send email
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[contact.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        logger.info(f"Contact confirmation email sent to {contact.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send contact confirmation email: {str(e)}")
        return False

def send_admin_booking_notification(booking):
    """
    Send new booking notification to admin
    """
    try:
        # Emergency bookings get priority subject
        if booking.service.is_emergency:
            subject = f"🚨 EMERGENCY BOOKING - {booking.service.name} in {booking.service_area.name}"
        else:
            subject = f"New Booking - {booking.service.name} in {booking.service_area.name}"
        
        # Handle preferred_date formatting
        preferred_date_str = "Not specified"
        if booking.preferred_date:
            try:
                # Convert to local timezone if timezone-aware
                if hasattr(booking.preferred_date, 'astimezone'):
                    local_date = timezone.localtime(booking.preferred_date)
                else:
                    local_date = booking.preferred_date
                
                # Format as user-friendly string with date and time
                preferred_date_str = local_date.strftime('%B %d, %Y at %I:%M %p')
            except Exception as e:
                logger.warning(f"Error formatting preferred_date: {e}")
                preferred_date_str = str(booking.preferred_date)
        
        # Render HTML email
        html_content = render_to_string('emails/admin_booking_notification.html', {
            'booking': booking,
            'preferred_date_formatted': preferred_date_str
        })
        
        # Create text version for admin
        urgency_text = "🚨 EMERGENCY" if booking.service.is_emergency else booking.get_urgency_display()
        text_content = f"""
        NEW BOOKING ALERT - SPRO Plumbing
        
        Customer: {booking.customer_name}
        Phone: {booking.phone}
        Email: {booking.email}
        Service: {booking.service.name}
        Location: {booking.service_area.name}
        Urgency: {urgency_text}
        Preferred Date: {preferred_date_str}
        Address: {booking.address}
        
        Description: {booking.description or 'No description provided'}
        
        ACTION REQUIRED: Call customer at {booking.phone}
        """
        
        # Send to admin email
        admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@sproplumbing.com')
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[admin_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        logger.info(f"Admin notification email sent for booking #{booking.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send admin notification email: {str(e)}")
        return False

def send_admin_contact_notification(contact):
    """
    Send new contact message notification to admin
    """
    try:
        subject = f"New Contact Message - {contact.subject} from {contact.service_area.name}"
        
        text_content = f"""
        NEW CONTACT MESSAGE - SPRO Plumbing
        
        Name: {contact.name}
        Email: {contact.email}
        Phone: {contact.phone or 'Not provided'}
        Location: {contact.service_area.name}
        Subject: {contact.subject}
        
        Message:
        {contact.message}
        
        Submitted: {contact.created_at.strftime('%B %d, %Y at %I:%M %p')}
        """
        
        # Send to admin email
        admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@sproplumbing.com')
        
        send_mail(
            subject=subject,
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[admin_email],
            fail_silently=False
        )
        
        logger.info(f"Admin contact notification email sent for message from {contact.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send admin contact notification email: {str(e)}")
        return False
