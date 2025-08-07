from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils.text import slugify
from .models import ServiceArea, Review, TrustBadge
from services.models import Service, Testimonial
from bookings.models import Booking, ContactMessage
from django.contrib import messages
from django.shortcuts import redirect
from core.email_utils import (
    send_booking_confirmation_email, 
    send_contact_confirmation_email,
    send_admin_booking_notification,
    send_admin_contact_notification
)
from main.forms import BookingForm, ContactForm

def get_service_area_by_slug(location_slug):
    """Find ServiceArea by matching slugified name"""
    for area in ServiceArea.objects.filter(is_active=True):
        if slugify(area.name) == location_slug:
            return area
    raise Http404("Service area not found")

def location_home(request, location_slug=None):
    if location_slug:
        service_area = get_service_area_by_slug(location_slug)
    else:
        service_area = ServiceArea.objects.filter(is_active=True).first()
    

    
    services = Service.objects.all()[:4]
    testimonials = Testimonial.objects.filter(location=service_area)
    reviews = Review.objects.filter(service_area=service_area, is_featured=True)[:3] if service_area else []
    trust_badges = TrustBadge.objects.filter(is_active=True)
    
    # Calculate average rating
    avg_rating = 0
    total_reviews = Review.objects.filter(service_area=service_area).count() if service_area else 0
    if total_reviews > 0:
        avg_rating = sum([r.rating for r in Review.objects.filter(service_area=service_area)]) / total_reviews
    
    # Add slug to service_area for template URLs
    if service_area:
        service_area.slug = slugify(service_area.name)
    
    context = {
        'service_area': service_area,
        'services': services,
        'testimonials': testimonials,
        'reviews': reviews,
        'trust_badges': trust_badges,
        'avg_rating': round(avg_rating, 1),
        'total_reviews': total_reviews,
    }
    return render(request, 'location_home.html', context)

def location_services(request, location_slug):
    service_area = get_service_area_by_slug(location_slug)
    services = Service.objects.all()
    emergency_services = Service.objects.filter(is_emergency=True)
    regular_services = Service.objects.filter(is_emergency=False)
    
    # Add slug to service_area for template URLs
    if service_area:
        service_area.slug = slugify(service_area.name)
    
    context = {
        'service_area': service_area,
        'services': services,
        'emergency_services': emergency_services,
        'regular_services': regular_services,
    }
    return render(request, 'location_services.html', context)

def location_booking(request, location_slug):
    service_area = get_service_area_by_slug(location_slug)
    
    if request.method == 'POST':
        # Create form data with service_area pre-filled
        form_data = request.POST.copy()
        form_data['service_area'] = service_area.id
        
        form = BookingForm(form_data)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.service_area = service_area
            booking.save()
            
            # Send confirmation email to customer
            try:
                email_sent = send_booking_confirmation_email(booking)
                admin_notified = send_admin_booking_notification(booking)
            except Exception as e:
                email_sent = False
            
            # Create enhanced success message with portal information
            portal_link = request.build_absolute_uri('/portal/login/')
            
            if email_sent:
                success_message = f'Booking request submitted successfully for {service_area.name}! Check your email for confirmation. Visit our Customer Portal at {portal_link} to track your booking status. We will contact you soon to confirm your appointment.'
            else:
                success_message = f'Booking request submitted successfully for {service_area.name}! Create an account in our Customer Portal at {portal_link} to track your booking status. We will contact you soon to confirm your appointment.'
            
            messages.success(request, success_message)
            return redirect('location_booking', location_slug=slugify(service_area.name))
        else:
            # Form has validation errors
            messages.error(request, 'Please correct the errors below and try again.')
    else:
        form = BookingForm()
    
    services = Service.objects.all()
    
    # Add slug to service_area for template URLs
    if service_area:
        service_area.slug = slugify(service_area.name)
    
    context = {
        'service_area': service_area,
        'services': services,
        'form': form
    }
    return render(request, 'location_booking.html', context)

def location_contact(request, location_slug):
    service_area = get_service_area_by_slug(location_slug)
    
    if request.method == 'POST':
        # Create form data with service_area pre-filled
        form_data = request.POST.copy()
        form_data['service_area'] = service_area.id
        
        form = ContactForm(form_data)
        if form.is_valid():
            contact_message = form.save(commit=False)
            contact_message.service_area = service_area
            contact_message.save()
            
            # Send confirmation email to customer
            try:
                email_sent = send_contact_confirmation_email(contact_message)
                admin_notified = send_admin_contact_notification(contact_message)
            except Exception as e:
                email_sent = False
            
            # Create enhanced success message with portal information
            portal_link = request.build_absolute_uri('/portal/login/')
            
            if email_sent:
                success_message = f'Message sent successfully from {service_area.name}! Check your email for confirmation. Visit our Customer Portal at {portal_link} to track communications. We will get back to you soon.'
            else:
                success_message = f'Message sent successfully from {service_area.name}! Create an account in our Customer Portal at {portal_link} to track communications. We will get back to you soon.'
            
            messages.success(request, success_message)
            return redirect('location_contact', location_slug=slugify(service_area.name))
        else:
            # Form has validation errors
            messages.error(request, 'Please correct the errors below and try again.')
    else:
        form = ContactForm()
    
    # Add slug to service_area for template URLs
    if service_area:
        service_area.slug = slugify(service_area.name)
    
    context = {
        'service_area': service_area,
        'form': form
    }
    return render(request, 'location_contact.html', context)