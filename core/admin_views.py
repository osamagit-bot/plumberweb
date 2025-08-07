from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
import json
from bookings.models import Booking
from quotes.models import QuoteRequest

def staff_required(view_func):
    """Decorator to ensure user is staff"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper

@require_http_methods(["PUT"])
def booking_status_api(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    try:
        data = json.loads(request.body)
        booking.status = data.get('status')
        
        # Auto-confirm when status is confirmed, in_progress, or completed
        if booking.status in ['confirmed', 'in_progress', 'completed']:
            booking.is_confirmed = True
        elif booking.status in ['pending', 'cancelled']:
            booking.is_confirmed = False
            
        booking.save()
        
        return JsonResponse({'success': True, 'message': 'Booking updated successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_http_methods(["PUT"])
def quote_status_api(request, quote_id):
    quote = get_object_or_404(QuoteRequest, id=quote_id)
    
    try:
        data = json.loads(request.body)
        quote.status = data.get('status')
        quote.save()
        
        return JsonResponse({'success': True, 'message': 'Quote updated successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)