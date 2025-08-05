from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Prefetch
from django.utils.text import slugify
from services.models import Service, Testimonial, FAQ
from areas.models import ServiceArea
from bookings.models import Booking, ContactMessage
from .models import GalleryImage
from .forms import BookingForm, ContactForm
from core.email_utils import (
    send_booking_confirmation_email, 
    send_contact_confirmation_email,
    send_admin_booking_notification,
    send_admin_contact_notification
)


def home(request):
    # Optimized queries with select_related and ordering
    services = (Service.objects
                .select_related()
                .order_by('-created_at')[:4])
    
    testimonials = (Testimonial.objects
                   .select_related('service', 'location')
                   .order_by('-created_at'))
    
    faqs = (FAQ.objects
            .filter(is_active=True)
            .order_by('order', 'created_at')[:6])
    
    service_areas = ServiceArea.objects.filter(is_active=True).order_by('name')
    
    # Add slug property to each service area for template URLs
    for area in service_areas:
        area.slug = slugify(area.name)
    
    context = {
        'services': services,
        'testimonials': testimonials,
        'faqs': faqs,
        'service_areas': service_areas,
    }
    return render(request, 'home.html', context)


def services_view(request):
    # Renamed from 'services' to avoid naming conflict with Service model
    all_services = Service.objects.all().order_by('name')
    emergency_services = Service.objects.filter(is_emergency=True).order_by('name')
    regular_services = Service.objects.filter(is_emergency=False).order_by('name')
    
    context = {
        'services': all_services,
        'emergency_services': emergency_services,
        'regular_services': regular_services,
    }
    return render(request, 'services.html', context)


def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            
            # Send confirmation email to customer
            email_sent = send_booking_confirmation_email(booking)
            
            # Send notification to admin
            admin_notified = send_admin_booking_notification(booking)
            
            if email_sent:
                messages.success(
                    request, 
                    'Booking request submitted successfully! Check your email for confirmation details. We will contact you soon.'
                )
            else:
                messages.success(
                    request, 
                    'Booking request submitted successfully! We will contact you soon.'
                )
            return redirect('booking')
        else:
            messages.error(
                request, 
                'Please correct the errors below and try again.'
            )
    else:
        form = BookingForm()
    
    # Optimized query for services
    services = Service.objects.all().order_by('name')
    context = {
        'form': form,
        'services': services
    }
    return render(request, 'booking.html', context)


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send confirmation email to customer
            email_sent = send_contact_confirmation_email(contact_message)
            
            # Send notification to admin
            admin_notified = send_admin_contact_notification(contact_message)
            
            if email_sent:
                messages.success(
                    request, 
                    'Message sent successfully! Check your email for confirmation. We will get back to you soon.'
                )
            else:
                messages.success(
                    request, 
                    'Message sent successfully! We will get back to you soon.'
                )
            return redirect('contact')
        else:
            messages.error(
                request, 
                'Please correct the errors below and try again.'
            )
    else:
        form = ContactForm()
    
    context = {'form': form}
    return render(request, 'contact.html', context)


def gallery_view(request):
    # Get filter parameters
    category_filter = request.GET.get('category', 'all')
    service_filter = request.GET.get('service', 'all')
    location_filter = request.GET.get('location', 'all')
    
    # Base queryset
    images = GalleryImage.objects.filter(is_active=True).select_related('service', 'location')
    
    # Apply filters
    if category_filter != 'all':
        images = images.filter(category=category_filter)
    if service_filter != 'all':
        images = images.filter(service_id=service_filter)
    if location_filter != 'all':
        images = images.filter(location_id=location_filter)
    
    # Get filter options
    categories = GalleryImage.CATEGORY_CHOICES
    services = Service.objects.all().order_by('name')
    locations = ServiceArea.objects.filter(is_active=True).order_by('name')
    
    # Get featured images for hero section
    featured_images = GalleryImage.objects.filter(is_active=True, is_featured=True)[:6]
    
    context = {
        'images': images,
        'featured_images': featured_images,
        'categories': categories,
        'services': services,
        'locations': locations,
        'current_category': category_filter,
        'current_service': service_filter,
        'current_location': location_filter,
    }
    return render(request, 'gallery.html', context)