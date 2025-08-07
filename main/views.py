from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Prefetch, Avg, Count
from django.utils.text import slugify
from django.utils.html import escape
from django.core.exceptions import ValidationError
from django_ratelimit.decorators import ratelimit
import logging

logger = logging.getLogger(__name__)
from services.models import Service, Testimonial, FAQ
from areas.models import ServiceArea
from bookings.models import Booking, ContactMessage
from .models import GalleryImage
from .forms import BookingForm, ContactForm, CustomerFeedbackForm
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
    
    # Get featured testimonials with rating statistics
    testimonials = (Testimonial.objects
                   .filter(is_approved=True, is_featured=True)
                   .select_related('service', 'location')
                   .order_by('-created_at')[:6])
    
    # Calculate overall rating and review count
    rating_stats = Testimonial.objects.filter(is_approved=True).aggregate(
        avg_rating=Avg('rating'),
        total_reviews=Count('id')
    )
    
    overall_rating = rating_stats['avg_rating']
    if overall_rating:
        overall_rating = round(overall_rating, 1)
    
    faqs = (FAQ.objects
            .filter(is_active=True)
            .order_by('order', 'created_at')[:6])
    
    service_areas = ServiceArea.objects.filter(is_active=True).order_by('name')
    
    # Add slug property to each service area for template URLs
    for area in service_areas:
        area.slug = slugify(area.name)
    
    # Get review platform URLs (from first active service area)
    google_business_url = yelp_url = trustpilot_url = reddit_url = None
    if service_areas.exists():
        first_area = service_areas.first()
        google_business_url = first_area.google_business_url if first_area.google_business_url else None
        yelp_url = first_area.yelp_url if first_area.yelp_url else None
        trustpilot_url = first_area.trustpilot_url if first_area.trustpilot_url else None
        reddit_url = first_area.reddit_url if first_area.reddit_url else None
    
    context = {
        'services': services,
        'testimonials': testimonials,
        'overall_rating': overall_rating,
        'total_reviews': rating_stats['total_reviews'],
        'faqs': faqs,
        'service_areas': service_areas,
        'google_business_url': google_business_url,
        'yelp_url': yelp_url,
        'trustpilot_url': trustpilot_url,
        'reddit_url': reddit_url,
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


# @ratelimit(key='ip', rate='5/m', method='POST')  # Enable for production
def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            
            # Send confirmation email to customer
            try:
                email_sent = send_booking_confirmation_email(booking)
                admin_notified = send_admin_booking_notification(booking)
                logger.info(f'Booking created: {booking.id}')
            except Exception as e:
                logger.error(f'Email sending failed for booking {booking.id}: {str(e)}')
                email_sent = False
            
            # Create enhanced success message with portal information
            portal_link = request.build_absolute_uri('/portal/login/')
            
            if email_sent:
                success_message = f'Booking request submitted successfully! Check your email for confirmation details. Visit our Customer Portal at {portal_link} to track your booking status. We will contact you soon to confirm your appointment.'
            else:
                success_message = f'Booking request submitted successfully! Create an account in our Customer Portal at {portal_link} to track your booking status. We will contact you soon to confirm your appointment.'
            
            messages.success(request, success_message)
            return redirect('main:booking')
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


# @ratelimit(key='ip', rate='5/m', method='POST')  # Enable for production
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send confirmation email to customer
            try:
                email_sent = send_contact_confirmation_email(contact_message)
                admin_notified = send_admin_contact_notification(contact_message)
                logger.info(f'Contact message created: {contact_message.id}')
            except Exception as e:
                logger.error(f'Email sending failed for contact {contact_message.id}: {str(e)}')
                email_sent = False
            
            # Create enhanced success message with portal information
            portal_link = request.build_absolute_uri('/portal/login/')
            
            if email_sent:
                success_message = f'Message sent successfully! Check your email for confirmation. Visit our Customer Portal at {portal_link} to track communications. We will get back to you soon.'
            else:
                success_message = f'Message sent successfully! Create an account in our Customer Portal at {portal_link} to track communications. We will get back to you soon.'
            
            messages.success(request, success_message)
            return redirect('main:contact')
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
    # Get filter parameters with validation
    category_filter = escape(request.GET.get('category', 'all'))
    service_filter = escape(request.GET.get('service', 'all'))
    location_filter = escape(request.GET.get('location', 'all'))
    
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


# @ratelimit(key='ip', rate='3/m', method='POST')  # Enable for production
def feedback_view(request):
    """Customer feedback form view"""
    if request.method == 'POST':
        form = CustomerFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.is_approved = False  # Require admin approval
            feedback.save()
            
            messages.success(
                request, 
                'Thank you for your feedback! Your review has been submitted and will be published after approval.'
            )
            return redirect('main:feedback')
        else:
            messages.error(
                request, 
                'Please correct the errors below and try again.'
            )
    else:
        form = CustomerFeedbackForm()
    
    context = {'form': form}
    return render(request, 'feedback.html', context)