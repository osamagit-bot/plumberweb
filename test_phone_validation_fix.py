#!/usr/bin/env python
"""
Test script to verify phone validation is working with form field overrides
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from main.forms import BookingForm, ContactForm
from services.models import Service
from areas.models import ServiceArea
from django.utils import timezone

def test_phone_validation_fix():
    print("Testing phone validation fix with form field overrides...")
    print("=" * 70)
    
    # Get or create test data
    service, _ = Service.objects.get_or_create(
        name="Test Service",
        defaults={
            'description': 'Test service for validation',
            'is_active': True
        }
    )
    
    service_area, _ = ServiceArea.objects.get_or_create(
        name="Test Area",
        defaults={
            'phone': '+15062345678',
            'email': 'test@example.com',
            'address': '123 Test St',
            'is_active': True
        }
    )
    
    # Test problematic phone formats
    test_phones = [
        "(506) 234-5678",
        "506-234-5678", 
        "506.234.5678",
        "506 234 5678",
        "5062345678",
        "+1 506 234 5678",
        "+1-506-234-5678",
        "1-506-234-5678",
    ]
    
    print("Testing BookingForm with overridden phone field...")
    print("-" * 50)
    
    for phone in test_phones:
        print(f"Testing phone: '{phone}'")
        
        form_data = {
            'customer_name': 'John Doe',
            'email': 'john@example.com',
            'phone': phone,
            'address': '123 Main St, Test City',
            'service': service.id,
            'service_area': service_area.id,
            'urgency': 'medium',
            'preferred_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M'),
            'description': 'Test booking description'
        }
        
        form = BookingForm(form_data)
        
        # Check if the phone field is a CharField (our override)
        phone_field = form.fields['phone']
        print(f"  Phone field type: {type(phone_field).__name__}")
        
        if form.is_valid():
            print(f"  ✓ PASS - Cleaned to: '{form.cleaned_data['phone']}'")
            try:
                booking = form.save()
                print(f"  ✓ PASS - Saved with ID: {booking.id}")
                print(f"  ✓ PASS - Database phone: '{booking.phone}'")
                booking.delete()  # Clean up
            except Exception as e:
                print(f"  ✗ FAIL - Save error: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"  ✗ FAIL - Form errors: {dict(form.errors)}")
            # Check if it's still a PhoneNumberField validation error
            if 'phone' in form.errors:
                print(f"  ✗ Phone field still using PhoneNumberField validation!")
        print()
    
    print("\nTesting ContactForm with overridden phone field...")
    print("-" * 50)
    
    for phone in test_phones[:3]:  # Test fewer for contact form
        print(f"Testing phone: '{phone}'")
        
        contact_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': phone,
            'subject': 'Test Subject',
            'message': 'Test message',
            'service_area': service_area.id
        }
        
        contact_form = ContactForm(contact_data)
        
        # Check if the phone field is a CharField (our override)
        phone_field = contact_form.fields['phone']
        print(f"  Phone field type: {type(phone_field).__name__}")
        
        if contact_form.is_valid():
            print(f"  ✓ PASS - Cleaned to: '{contact_form.cleaned_data['phone']}'")
            try:
                contact = contact_form.save()
                print(f"  ✓ PASS - Saved with ID: {contact.id}")
                print(f"  ✓ PASS - Database phone: '{contact.phone}'")
                contact.delete()  # Clean up
            except Exception as e:
                print(f"  ✗ FAIL - Save error: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"  ✗ FAIL - Form errors: {dict(contact_form.errors)}")
        print()
    
    print("=" * 70)
    print("✅ Phone validation fix test completed!")
    print("\nIf you're still seeing validation errors:")
    print("1. Restart your Django development server")
    print("2. Clear browser cache completely")
    print("3. Try in incognito/private browsing mode")
    print("4. Check browser developer console for JavaScript errors")

if __name__ == "__main__":
    test_phone_validation_fix()