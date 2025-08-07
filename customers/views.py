from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import CustomerRegistrationForm, CustomerProfileForm, QuickBookingForm
from .models import CustomerProfile, CustomerDocument
from bookings.models import Booking
from quotes.models import QuoteRequest
from bookings.models import ContactMessage


def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your account has been created successfully! Please login with your credentials.')
            return redirect('customers:login')
    else:
        form = CustomerRegistrationForm()
    
    return render(request, 'customers/register.html', {'form': form})


@login_required
def dashboard(request):
    customer_profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    # Get recent bookings
    recent_bookings = Booking.objects.filter(
        Q(email=request.user.email) | Q(customer=customer_profile)
    ).order_by('-created_at')[:5]
    
    # Get recent quotes
    recent_quotes = QuoteRequest.objects.filter(
        Q(email=request.user.email) | Q(customer=customer_profile)
    ).order_by('-created_at')[:5]
    
    # Get recent documents
    recent_documents = CustomerDocument.objects.filter(
        customer=customer_profile,
        is_public=True
    ).order_by('-created_at')[:5]
    
    # Statistics
    total_bookings = Booking.objects.filter(
        Q(email=request.user.email) | Q(customer=customer_profile)
    ).count()
    
    total_quotes = QuoteRequest.objects.filter(
        Q(email=request.user.email) | Q(customer=customer_profile)
    ).count()
    
    pending_bookings = Booking.objects.filter(
        Q(email=request.user.email) | Q(customer=customer_profile),
        is_confirmed=False
    ).count()
    
    context = {
        'customer_profile': customer_profile,
        'recent_bookings': recent_bookings,
        'recent_quotes': recent_quotes,
        'recent_documents': recent_documents,
        'total_bookings': total_bookings,
        'total_quotes': total_quotes,
        'pending_bookings': pending_bookings,
    }
    
    return render(request, 'customers/dashboard.html', context)


@login_required
def profile(request):
    customer_profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('customers:profile')
    else:
        form = CustomerProfileForm(instance=customer_profile)
    
    return render(request, 'customers/profile.html', {
        'form': form,
        'customer_profile': customer_profile
    })


@login_required
def bookings(request):
    customer_profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    # Get all bookings for this customer
    bookings_list = Booking.objects.filter(
        Q(email=request.user.email) | Q(customer=customer_profile)
    ).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(bookings_list, 10)
    page_number = request.GET.get('page')
    bookings_page = paginator.get_page(page_number)
    
    return render(request, 'customers/bookings.html', {
        'bookings': bookings_page,
        'customer_profile': customer_profile
    })


@login_required
def booking_detail(request, booking_id):
    customer_profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        email=request.user.email
    )
    
    return render(request, 'customers/booking_detail.html', {
        'booking': booking,
        'customer_profile': customer_profile
    })


@login_required
def quotes(request):
    customer_profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    # Get all quotes for this customer
    quotes_list = QuoteRequest.objects.filter(
        Q(email=request.user.email) | Q(customer=customer_profile)
    ).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(quotes_list, 10)
    page_number = request.GET.get('page')
    quotes_page = paginator.get_page(page_number)
    
    return render(request, 'customers/quotes.html', {
        'quotes': quotes_page,
        'customer_profile': customer_profile
    })


@login_required
def quote_detail(request, quote_id):
    customer_profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    quote = get_object_or_404(
        QuoteRequest,
        id=quote_id,
        email=request.user.email
    )
    
    return render(request, 'customers/quote_detail.html', {
        'quote': quote,
        'customer_profile': customer_profile
    })


@login_required
def accept_quote(request, quote_id):
    customer_profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    quote = get_object_or_404(
        QuoteRequest,
        id=quote_id,
        email=request.user.email,
        status='quoted'
    )
    
    if request.method == 'POST':
        # Accept the quote
        quote.status = 'accepted'
        quote.save()
        
        # Redirect to quick booking with pre-filled data
        messages.success(request, f'Quote accepted! Please schedule your {quote.service.name} service.')
        return redirect('customers:book_from_quote', quote_id=quote.id)
    
    return redirect('customers:quote_detail', quote_id=quote_id)


@login_required
def book_from_quote(request, quote_id):
    customer_profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    quote = get_object_or_404(
        QuoteRequest,
        id=quote_id,
        email=request.user.email,
        status='accepted'
    )
    
    if request.method == 'POST':
        form = QuickBookingForm(request.POST)
        if form.is_valid():
            from datetime import datetime, time
            from django.utils import timezone
            
            preferred_date = form.cleaned_data['preferred_date']
            preferred_time_choice = form.cleaned_data['preferred_time']
            
            if preferred_time_choice == 'morning':
                preferred_time = time(9, 0)
            elif preferred_time_choice == 'afternoon':
                preferred_time = time(14, 0)
            else:
                preferred_time = time(17, 0)
                
            preferred_datetime = timezone.make_aware(datetime.combine(preferred_date, preferred_time))
            
            # Create booking from accepted quote
            booking = Booking.objects.create(
                customer=customer_profile,
                customer_name=customer_profile.full_name,
                email=request.user.email,
                phone=customer_profile.phone or '',
                address=customer_profile.full_address or quote.address,
                service=quote.service,
                preferred_date=preferred_datetime,
                urgency=form.cleaned_data.get('urgency', 'medium'),
                description=f"Booking from accepted quote #{quote.id}. {form.cleaned_data.get('description', '')}",
                status='pending'
            )
            
            messages.success(request, f'Service booked successfully! Reference: #{booking.id}')
            return redirect('customers:booking_detail', booking_id=booking.id)
    else:
        # Pre-fill form with quote data
        initial_data = {
            'service': quote.service.id,
            'description': f'Service from accepted quote #{quote.id}'
        }
        form = QuickBookingForm(initial=initial_data)
    
    return render(request, 'customers/quick_booking.html', {
        'form': form,
        'customer_profile': customer_profile,
        'quote': quote,
        'from_quote': True
    })


@login_required
def quick_booking(request):
    customer_profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = QuickBookingForm(request.POST)
        if form.is_valid():
            # Get the selected service
            from services.models import Service
            try:
                selected_service = Service.objects.get(id=form.cleaned_data['service'])
            except Service.DoesNotExist:
                messages.error(request, 'Selected service is not available.')
                return render(request, 'customers/quick_booking.html', {
                    'form': form,
                    'customer_profile': customer_profile
                })
            
            # Create preferred_date as datetime
            from datetime import datetime, time
            from django.utils import timezone
            preferred_date = form.cleaned_data['preferred_date']
            preferred_time_choice = form.cleaned_data['preferred_time']
            
            # Convert time choice to actual time
            if preferred_time_choice == 'morning':
                preferred_time = time(9, 0)  # 9:00 AM
            elif preferred_time_choice == 'afternoon':
                preferred_time = time(14, 0)  # 2:00 PM
            else:  # evening
                preferred_time = time(17, 0)  # 5:00 PM
                
            preferred_datetime = timezone.make_aware(datetime.combine(preferred_date, preferred_time))
            
            # Create a new booking
            booking = Booking.objects.create(
                customer=customer_profile,
                customer_name=customer_profile.full_name,
                email=request.user.email,
                phone=customer_profile.phone or '',
                address=customer_profile.full_address or 'Address not provided',
                service=selected_service,
                preferred_date=preferred_datetime,
                urgency='emergency' if form.cleaned_data['is_emergency'] else 'normal',
                description=form.cleaned_data['description'],
                status='pending'
            )
            
            messages.success(request, f'Your booking request has been submitted successfully! Reference: #{booking.id}')
            return redirect('customers:booking_detail', booking_id=booking.id)
    else:
        form = QuickBookingForm()
    
    return render(request, 'customers/quick_booking.html', {
        'form': form,
        'customer_profile': customer_profile
    })


@login_required
def cancel_booking(request, booking_id):
    customer_profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        email=request.user.email,
        status__in=['pending', 'confirmed']  # Only allow cancelling pending/confirmed bookings
    )
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f'Booking #{booking.id} has been cancelled successfully.')
        return redirect('customers:bookings')
    
    return redirect('customers:booking_detail', booking_id=booking_id)


@login_required
def service_history(request):
    from django.db.models import Count
    from datetime import datetime
    
    customer_profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    # Get completed bookings (service history)
    completed_bookings = Booking.objects.filter(
        Q(email=request.user.email) | Q(customer=customer_profile),
        status='completed'
    ).order_by('-updated_at')
    
    # Statistics
    total_services = completed_bookings.count()
    current_year = datetime.now().year
    services_this_year = completed_bookings.filter(updated_at__year=current_year).count()
    
    # Pagination
    paginator = Paginator(completed_bookings, 10)
    page_number = request.GET.get('page')
    history_page = paginator.get_page(page_number)
    
    return render(request, 'customers/service_history.html', {
        'history': history_page,
        'customer_profile': customer_profile,
        'total_services': total_services,
        'services_this_year': services_this_year,
    })
